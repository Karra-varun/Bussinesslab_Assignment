# AI Tech Consultant

**One connected AI system that knows your product, drafts customer replies, and turns client meetings into scopes of work.** Built for any software or SaaS business to replace $2,000 developer setup overhead with automated 10x-20x delivery.

---

## What It Does

The AI Tech Consultant connects three specialized tasks into one shared brain:

1. **The Knowledge Brain (Port 8001 · Python)**: Reads your public help center (Brilliant Directories), parses screenshot images, updates daily with sitemap diffs, purges deleted articles, and creates human expert tickets when confidence is low. Expert answers flow back into memory.
2. **The Inbox Agent (Port 8002 · TypeScript)**: Triages customer emails, calls Task 1's API for facts, and drafts replies in your company voice. Learns from human edits via Levenshtein diffing. After 20 unedited sends in a category, that category unlocks autonomous sending with safety circuit breakers.
3. **Meeting to Scope of Work (Port 8003 · Python)**: Multi-agent team (Consultant, Architect, Estimator, Diff Auditor) turns client meeting transcripts into scopes of work, task estimates, and client-ready proposals. Automatically verifies which requests are solved by native settings ($0) versus custom code ($125/hr), tracks meeting deltas, and isolates scope creep.

---

## How to Run with One Command

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Node.js 18+ (tested on Node v24)

### Quickstart

1. **Clone & Enter Repo**:
   ```bash
   cd ai-tech-consultant
   ```

2. **One-Command Launch**:
   - **Windows**:
     ```cmd
     run_all.bat
     ```
   - **macOS / Linux**:
     ```bash
     chmod +x run_all.sh && ./run_all.sh
     ```

3. **Open the Dashboards**:
   - **Executive Command Center**: [http://localhost:8000](http://localhost:8000)
   - **Task 1 Knowledge Brain Studio**: [http://localhost:8001](http://localhost:8001) *(Swagger API Docs: `/docs`)*
   - **Task 2 Inbox Agent Dashboard**: [http://localhost:8002](http://localhost:8002)
   - **Task 3 Meeting-to-SOW Studio**: [http://localhost:8003](http://localhost:8003) *(Swagger API Docs: `/docs`)*

---

## Running Automated Tests

Run the complete test suite across all three tasks with 100% passing results:

```bash
# Task 1 Tests (Knowledge Brain)
.\.venv\Scripts\pytest task1-knowledge-brain/tests/test_task1.py -v

# Task 2 Tests (TypeScript Inbox Agent)
cd task2-inbox-agent && npm test && cd ..

# Task 3 Tests (Multi-Agent Scope of Work)
.\.venv\Scripts\pytest task3-meeting-sow/tests/test_task3.py -v

# Run 70-Question Empirical Benchmark Evals
.\.venv\Scripts\python evals/run_evals.py
```

---

## Architecture at a Glance

```
                         ┌────────────────────────────────────────┐
                         │   Executive Command Portal (:8000)     │
                         └───────────────────┬────────────────────┘
                                             │
               ┌─────────────────────────────┼─────────────────────────────┐
               ▼                             ▼                             ▼
┌──────────────────────────────┐ ┌───────────────────────┐ ┌──────────────────────────────┐
│ Task 1: Knowledge Brain      │ │ Task 2: Inbox Agent   │ │ Task 3: Meeting-to-SOW       │
│ • Python FastAPI (:8001)     │ │ • TypeScript Node     │ │ • Python FastAPI (:8003)     │
│ • Sitemap Crawler & Sync     │ │   Express (:8002)     │ │ • Multi-Agent Team           │
│ • Hybrid RAG (BM25 + Dense)  │ │ • 52 Real Emails      │ │ • Settings ($0) vs Code      │
│ • Multimodal Vision / OCR    │ │ • Levenshtein Learner │ │ • Meeting 1 vs 3 Diffing     │
│ • Human Expert Ticket Queue  │ │ • 20-Streak Autonomy  │ │ • Scope Creep Gate           │
└──────────────┬───────────────┘ └───────────┬───────────┘ └──────────────┬───────────────┘
               ▲                             │                            │
               └─────────── REST API ────────┴──────────── REST API ──────┘
```

---

## Technology Stack

- **Task 1**: Python 3.14, FastAPI, Pydantic v2, HTTPX, BeautifulSoup4, AsyncIO, Pytest
- **Task 2**: TypeScript 5/7 (Strict Mode), Node.js, Express, CORS, Dotenv
- **Task 3**: Python 3.14, FastAPI, Multi-Agent Architecture, Markdown SOW Engine
- **Evaluation**: 70 Test Cases across Claude 3.5 Sonnet, Claude 3.5 Haiku, and Grounded RAG
