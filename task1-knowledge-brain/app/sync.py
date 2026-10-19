"""
Daily Incremental Sync Engine for Task 1: The Knowledge Brain.
Monitors sitemap.xml to detect:
1. Added pages -> crawls, chunks, and indexes.
2. Updated pages -> detects lastmod/hash diffs and refreshes index.
3. Removed pages -> purges immediately from memory, vector store, and search indices.
"""
import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx

from app.config import settings, STATE_FILE
from app.models import Article, SyncReport, SyncStatus
from app.scraper import scraper
from app.rag import rag_store

logger = logging.getLogger("sync_engine")


class IncrementalSyncEngine:
    def __init__(self):
        self.is_syncing: bool = False
        self.last_report: Optional[SyncReport] = None

    async def execute_sync(self, simulated_sitemap_urls: Optional[List[Dict[str, str]]] = None) -> SyncReport:
        """
        Execute incremental sync against the help center sitemap.
        Supports passing simulated sitemap URLs for testing additions/deletions.
        """
        if self.is_syncing:
            logger.warning("Sync already in progress.")
            return self.last_report or SyncReport(details=["Sync currently running."])

        self.is_syncing = True
        start_time = time.time()
        report = SyncReport()

        try:
            # Step 1: Discover sitemap URLs
            sitemap_items = simulated_sitemap_urls if simulated_sitemap_urls is not None else await scraper.fetch_sitemap_urls()
            report.total_scanned = len(sitemap_items)

            sitemap_url_map = {item["url"]: item.get("lastmod", "") for item in sitemap_items}
            stored_urls = dict(scraper.state.get("processed_urls", {}))

            added_urls: List[Dict[str, str]] = []
            updated_urls: List[Dict[str, str]] = []
            removed_urls: List[str] = []

            # Step 2: Identify Added & Updated
            for url, lastmod in sitemap_url_map.items():
                if url not in stored_urls:
                    added_urls.append({"url": url, "lastmod": lastmod})
                else:
                    stored_lastmod = stored_urls[url].get("lastmod")
                    if lastmod and stored_lastmod and lastmod != stored_lastmod:
                        updated_urls.append({"url": url, "lastmod": lastmod})

            # Step 3: Identify Removed (in stored state, but absent from sitemap)
            for url, info in stored_urls.items():
                if url not in sitemap_url_map:
                    # Ignore custom expert answer URLs from deletion
                    if not url.startswith("https://support.brilliantdirectories.com/support/expert-answers/"):
                        removed_urls.append(url)

            # Step 4: Handle Removals - PURGE FROM INDEX
            for url in removed_urls:
                art_id = stored_urls[url].get("article_id")
                if art_id:
                    rag_store.remove_article(art_id)
                    if art_id in scraper.state.get("article_index", {}):
                        del scraper.state["article_index"][art_id]
                del scraper.state["processed_urls"][url]
                report.removed += 1
                report.details.append(f"Purged removed article: {url} (ID: {art_id})")

            # Step 5: Handle Additions & Updates politely
            async with httpx.AsyncClient(timeout=25.0, headers=scraper.headers, follow_redirects=True) as client:
                for item in added_urls[:settings.max_scrape_batch]:
                    art = await scraper.scrape_article(client, item["url"], item.get("lastmod", ""))
                    if art:
                        rag_store.index_articles([art])
                        scraper.state["processed_urls"][item["url"]] = {
                            "lastmod": item.get("lastmod"),
                            "hash": art.content_hash,
                            "article_id": art.id
                        }
                        scraper.state["article_index"][art.id] = art.dict()
                        report.added += 1
                        report.details.append(f"Added new article: {art.title} ({art.url})")

                for item in updated_urls[:settings.max_scrape_batch]:
                    art = await scraper.scrape_article(client, item["url"], item.get("lastmod", ""))
                    if art:
                        rag_store.index_articles([art])
                        scraper.state["processed_urls"][item["url"]] = {
                            "lastmod": item.get("lastmod"),
                            "hash": art.content_hash,
                            "article_id": art.id
                        }
                        scraper.state["article_index"][art.id] = art.dict()
                        report.updated += 1
                        report.details.append(f"Refreshed updated article: {art.title} ({art.url})")

            # Step 6: Save state
            scraper.state["last_sitemap_check"] = datetime.utcnow().isoformat()
            scraper._save_state()

        except Exception as e:
            logger.error(f"Sync error: {e}")
            report.details.append(f"Sync error encountered: {str(e)}")
        finally:
            report.execution_time_sec = round(time.time() - start_time, 2)
            self.is_syncing = False
            self.last_report = report

        return report

    def get_status(self) -> SyncStatus:
        return SyncStatus(
            status="syncing" if self.is_syncing else "idle",
            total_articles=len(rag_store.articles),
            last_sync_time=scraper.state.get("last_sitemap_check"),
            sitemap_url=settings.sitemap_url,
            categories=scraper.state.get("categories", [])
        )


sync_engine = IncrementalSyncEngine()
