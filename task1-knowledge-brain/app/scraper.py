"""
Polite Web Scraper and Sitemap Parser for Brilliant Directories Solution Center.
Features:
- Rate limiting and polite delays to prevent server overload.
- Batch processing with checkpointing into sync_state.json.
- Resumable: if stopped halfway, continues from where it left off.
- Hierarchy extraction: Category -> Folder -> Article.
- Multimodal extraction: finds <img> tags, alt texts, and UI screenshot contexts.
"""
import asyncio
import hashlib
import json
import logging
import re
from typing import List, Dict, Any, Optional
from xml.etree import ElementTree as ET
import httpx
from bs4 import BeautifulSoup

from app.config import settings, STATE_FILE, ARTICLES_DIR
from app.models import Article, ImageMetadata
from app.seeded_articles import SEEDED_ARTICLES

logger = logging.getLogger("scraper")
logging.basicConfig(level=logging.INFO)


class PoliteHelpCenterScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "AI-Tech-Consultant-PoliteBot/1.0 (Ethical Knowledge Scraper; +https://businesslabs.ai)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        self.state: Dict[str, Any] = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load sync_state: {e}")
        return {
            "last_sitemap_check": None,
            "processed_urls": {},
            "article_index": {},
            "categories": [],
            "resume_checkpoint": 0
        }

    def _save_state(self):
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving sync state: {e}")

    async def fetch_sitemap_urls(self) -> List[Dict[str, str]]:
        """Fetch and parse support sitemap to retrieve article URLs and lastmod."""
        urls = []
        try:
            async with httpx.AsyncClient(timeout=20.0, headers=self.headers, follow_redirects=True) as client:
                resp = await client.get(settings.sitemap_url)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
                    for url_tag in root.findall("sm:url", ns):
                        loc = url_tag.find("sm:loc", ns)
                        lastmod = url_tag.find("sm:lastmod", ns)
                        if loc is not None and loc.text:
                            loc_str = loc.text.strip()
                            lastmod_str = lastmod.text.strip() if lastmod is not None and lastmod.text else ""
                            # Only target article solutions
                            if "/support/solutions/articles/" in loc_str:
                                urls.append({"url": loc_str, "lastmod": lastmod_str})
                    logger.info(f"Discovered {len(urls)} article URLs from live sitemap.")
                    return urls
        except Exception as e:
            logger.warning(f"Could not reach live sitemap ({e}). Using seeded sitemap references.")

        # Fallback to seeded articles list if offline or blocked
        for sa in SEEDED_ARTICLES:
            urls.append({"url": sa.url, "lastmod": sa.last_modified or ""})
        return urls

    async def scrape_article(self, client: httpx.AsyncClient, url: str, lastmod: str = "") -> Optional[Article]:
        """Politely scrape an individual article page with error isolation and delay."""
        try:
            # Polite pause to prevent server strain
            await asyncio.sleep(settings.request_delay_seconds)
            resp = await client.get(url)
            if resp.status_code == 404:
                return None
            if resp.status_code != 200:
                logger.warning(f"Non-200 status {resp.status_code} for {url}")
                return None

            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Title extraction
            title_elem = soup.find("h1") or soup.find("title")
            title = title_elem.get_text(strip=True) if title_elem else "Help Center Article"
            title = re.sub(r"\s*:\s*Brilliant Directories.*$", "", title, flags=re.I)

            # Extract article ID from URL
            m = re.search(r"/articles/(\d+)", url)
            article_id = m.group(1) if m else hashlib.md5(url.encode()).hexdigest()[:10]

            # Breadcrumbs extraction (Category / Folder)
            breadcrumbs = []
            crumb_elements = soup.select(".breadcrumb li, .breadcrumb a, [class*='breadcrumb'] a")
            for c in crumb_elements:
                txt = c.get_text(strip=True)
                if txt and txt.lower() not in ["home", "solutions"]:
                    breadcrumbs.append(txt)

            category = breadcrumbs[0] if len(breadcrumbs) > 0 else "General"
            folder = breadcrumbs[1] if len(breadcrumbs) > 1 else (breadcrumbs[0] if breadcrumbs else "Overview")

            # Extract main article content body
            body_elem = soup.find("div", class_=re.compile(r"article-body|content|solution-body|entry-content", re.I))
            if not body_elem:
                body_elem = soup.find("article") or soup.find("main") or soup.body

            content_text = body_elem.get_text(separator=" ", strip=True) if body_elem else ""
            content_html = str(body_elem) if body_elem else ""

            # Multimodal extraction: Find screenshots and UI annotations
            screenshots: List[ImageMetadata] = []
            if body_elem:
                for img in body_elem.find_all("img"):
                    src = img.get("src") or img.get("data-src")
                    if src and not src.startswith("data:"):
                        alt = img.get("alt", "").strip()
                        # UI context from preceding paragraph or parent caption
                        parent_text = img.parent.get_text(strip=True) if img.parent else ""
                        screenshots.append(ImageMetadata(
                            url=src,
                            alt=alt,
                            caption=alt or "Screenshot illustrating article settings",
                            ocr_text=f"UI context: {alt}",
                            ui_context=parent_text[:150] if parent_text else f"{category} > {folder}",
                            article_id=article_id
                        ))

            content_hash = hashlib.sha256(content_text.encode("utf-8")).hexdigest()

            article = Article(
                id=article_id,
                url=url,
                title=title,
                category=category,
                folder=folder,
                breadcrumbs=breadcrumbs,
                content_html=content_html[:5000],
                content_text=content_text,
                screenshots=screenshots,
                last_modified=lastmod,
                content_hash=content_hash,
                source="help_center"
            )
            return article

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None

    async def run_batch_scrape(self, batch_size: Optional[int] = None, force_refresh: bool = False) -> List[Article]:
        """Runs a batch scrape politely, resuming from checkpoint if previously stopped."""
        batch_limit = batch_size or settings.max_scrape_batch
        all_sitemap_urls = await self.fetch_sitemap_urls()
        
        # Check against existing state
        processed = self.state.get("processed_urls", {})
        pending_urls = []
        for item in all_sitemap_urls:
            url = item["url"]
            if force_refresh or url not in processed or processed[url].get("lastmod") != item["lastmod"]:
                pending_urls.append(item)

        logger.info(f"Total sitemap articles: {len(all_sitemap_urls)}. Pending to scrape/update: {len(pending_urls)}")

        results: List[Article] = []
        if not pending_urls:
            logger.info("Knowledge base is already up to date with sitemap.")
            return results

        async with httpx.AsyncClient(timeout=25.0, headers=self.headers, follow_redirects=True) as client:
            count = 0
            for item in pending_urls:
                if count >= batch_limit:
                    logger.info(f"Reached batch limit of {batch_limit}. Saving progress for next iteration.")
                    break
                url = item["url"]
                article = await self.scrape_article(client, url, item.get("lastmod", ""))
                if article:
                    results.append(article)
                    # Update state immediately for checkpoint resumption
                    self.state["processed_urls"][url] = {
                        "lastmod": item.get("lastmod"),
                        "hash": article.content_hash,
                        "article_id": article.id
                    }
                    self.state["article_index"][article.id] = article.dict()
                    if article.category not in self.state["categories"]:
                        self.state["categories"].append(article.category)
                    count += 1
                    self._save_state()

        logger.info(f"Batch scrape finished. Scraped {len(results)} new/updated articles.")
        return results

    def seed_initial_knowledge(self):
        """Seed the knowledge base with real Brilliant Directories articles if empty."""
        for sa in SEEDED_ARTICLES:
            if sa.id not in self.state["article_index"]:
                self.state["article_index"][sa.id] = sa.dict()
                self.state["processed_urls"][sa.url] = {
                    "lastmod": sa.last_modified,
                    "hash": sa.content_hash,
                    "article_id": sa.id
                }
                if sa.category not in self.state["categories"]:
                    self.state["categories"].append(sa.category)
        self._save_state()
        logger.info(f"Seeded knowledge base with {len(SEEDED_ARTICLES)} core articles.")


scraper = PoliteHelpCenterScraper()
# Ensure seeded articles are loaded on boot
scraper.seed_initial_knowledge()
