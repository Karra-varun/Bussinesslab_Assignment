# AI Collaboration Log (`AI_LOG.md`)
**Applied AI Engineering Development Record · October 2026**

---

## 1. Top 5 Most Useful Prompts

### Prompt 1: Multi-Agent SOW Deliberation Pipeline (Task 3)
> *"Design a team of 4 specialized agents for converting messy client transcripts into an approved Scope of Work. The first agent (Consultant) must extract raw client intent. The second (Architect) must query Task 1's REST API to check if each item is an existing product setting ($0) or custom code. The third (Estimator) breaks custom items into engineering tasks with developer roles, hours, and costs. The fourth (Diff Auditor) compares Meeting 1 baseline with Meeting 3 revisions to isolate out-of-scope creep into a separate change order quote. Output strictly typed Pydantic models."*
- **Why it worked**: Forced agent role separation and made Task 1 API validation mandatory before any engineering hours were quoted.

### Prompt 2: Polite Sitemap Scraper with Resumable Checkpoint (Task 1)
> *"Build an asynchronous, rate-limited scraper for support.brilliantdirectories.com/support/sitemap.xml. It must insert a polite 200ms delay between article requests, extract breadcrumb hierarchy (Category > Folder > Article), extract screenshots with parent UI context, and save processed URLs to sync_state.json with content hashes so that if stopped halfway, it resumes without re-scraping."*
- **Why it worked**: Prevented IP throttling while ensuring state persistence and multimodal screenshot awareness.

### Prompt 3: Levenshtein Learning Loop & 20-in-a-Row Autonomy Gate (Task 2)
> *"In TypeScript strict mode, build a learning engine for email replies. When a human sends a draft as-is (or with <5% character edit distance), increment an autonomy streak for that category. Once the streak reaches 20, unlock autonomous sending. If a human makes substantive edits or replaces the draft, calculate the diff, extract the reusable policy rule into a feedback database, and inject it into future prompts for that category. Include a circuit breaker to revoke autonomy if quality drops."*
- **Why it worked**: Produced an actionable mathematical definition for 'without changing' (Levenshtein similarity >= 0.95) and implemented true self-improvement.

### Prompt 4: Daily Incremental Sitemap Sync & Deletion Purge (Task 1)
> *"Implement daily sitemap synchronization. Compare the latest sitemap URLs against stored state. Categorize each URL as added, updated (via lastmod / SHA-256 hash diff), or removed. If an article was removed from the sitemap, purge it immediately from the vector index and search memory so it stops appearing in answers."*
- **Why it worked**: Kept the Knowledge Brain fresh every day and prevented embarrassing citations to deprecated features.

### Prompt 5: Dual-Model Cost & Latency Benchmark Engine (Evals)
> *"Write an automated evaluation runner that tests 70 questions across all 3 tasks. Compare Claude 3.5 Sonnet, Claude 3.5 Haiku, and a local deterministic Grounded RAG baseline. Report Quality (Accuracy %), Speed (Latency in ms), and Cost (USD and INR per 1,000 queries) with numbers, not adjectives."*
- **Why it worked**: Replaced subjective claims with hard empirical benchmark data justifying model selection per task.

---

## 2. One Time I Rejected the AI's Answer (and Why)

### The AI's Initial Proposal:
During the design of Task 1's RAG retrieval score calculation in `rag.py`, the AI proposed normalizing the BM25 lexical score by dividing by the highest-scoring document's BM25 score in the query:
```python
# REJECTED CODE:
normalized_bm25 = bm / max_bm25
combined_score = (0.65 * normalized_bm25) + (0.35 * sem)
```

### Why I Rejected It:
This normalization had a critical failure mode: if a user asked an out-of-domain nonsense question like *"How do I deploy an Ethereum smart contract on Mars?"*, the raw BM25 score was near zero (matching only tiny grammatical stop words like "do" or "on"). However, dividing by `max_bm25` artificially inflated that near-zero score to `1.0`! As a result, the chatbot returned a confidence score of `0.65+` on Martian quantum contracts instead of triggering the honest fallback gate.

### The Corrective Fix:
I rejected the formula and rewrote the retrieval scoring to:
1. Filter out English stopwords from query tokenization.
2. Require a minimum raw BM25 threshold (`max_bm25 > 0.0001`) and direct query token overlap before computing confidence.
3. If no substantive keywords match the help center corpus, return empty citations so the confidence evaluates to `0.0`, correctly triggering the honest fallback and escalating to a human expert ticket (`TICK-XXXX`).
