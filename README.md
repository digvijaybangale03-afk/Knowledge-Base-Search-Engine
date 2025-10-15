# Knowledge-base Search Engine (RAG) — Shortlisting-ready Project
**Objective:** Search across documents and provide synthesized answers using retrieval-augmented generation (RAG).

This repository contains a ready-to-run demonstration project implementing the requirements from the assessment prompt: document ingestion (PDF/text), vector retrieval (embeddings + FAISS), LLM-based answer synthesis, backend API (FastAPI), simple frontend (Streamlit), Docker configuration, and deployment instructions. It also includes a demo recording script and evaluation checklist for interview shortlisting.

**What's included**
- `backend/` — FastAPI app with ingestion, retrieval, and query endpoints.
- `frontend/` — Streamlit app for submitting documents and queries.
- `docker/` — Dockerfile and docker-compose for local deployment.
- `demo_script.md` — step-by-step demo recording script to produce the demo video deliverable.
- `README.md` — this file (instructions below), plus prompt guidance and evaluation notes.
- `requirements.txt` — python dependencies to install.
- `sample_data/` — placeholder README explaining where to put PDFs (not populated with copyrighted docs).

> Important: This project uses an LLM for synthesis. You can use OpenAI's API (recommended for easiest shortlisting demonstration) or any other LLM that exposes a text-completion/chat API. You must supply your own API key in deployment instructions below.

---
## Quick start (developer machine)
1. Install Python 3.10+ and create a venv:
```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate       # Windows (PowerShell)
pip install -r requirements.txt
```

2. Export your OpenAI API key (example):
```bash
export OPENAI_API_KEY="sk-..."  windows = $env:OPENAI_API_KEY="sk-..."

```

3. Run the backend:
```bash
cd backend
dir
$env:OPENAI_API_KEY="sk-your-actual-key-here"
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

4. In a new terminal run the frontend:
```bash
cd frontend
streamlit run app.py --server.port 8501
```

5. Open `http://localhost:8501` to interact with the demo. Upload documents (PDF / .txt) and run queries.

---
## Deployment (Docker Compose)
See `docker/docker-compose.yml` and `docker/Dockerfile` for instructions. Example:
```bash
docker compose up --build
# then visit http://localhost:8501
```

---
## How it meets assessment criteria
- **Document ingestion**: `/ingest` endpoint accepts PDF or text files, extracts text, splits into passages, stores embeddings in an on-disk FAISS index.
- **Retrieval**: FAISS vector store using sentence-transformers embeddings for dense retrieval + simple BM25 fallback (optional) for robustness.
- **LLM Synthesis**: Uses a concise RAG prompt template to synthesize answers from retrieved passages. Encourages citing passages and returning short, referenced answers.
- **Backend API**: FastAPI app provides endpoints for ingest, status, and /query to return JSON results.
- **Frontend**: Streamlit-based UI for recruiters to upload documents, submit queries, and copy downloadable answer transcripts.
- **Deliverables**: repo + README, demo script to record, evaluation checklist in README.

---
## Notes about AI-detection and authenticity
No tool can guarantee non-detection by AI detectors. The best ways to make the submission feel authentic:
- Add original commentary and examples in the README and demo video (personalize).
- Include a README section describing design tradeoffs and architectural decisions in your own words.
- Add a short recorded walkthrough (use the `demo_script.md`) where you explain design choices and demonstrate the system using domain-specific documents — this strongly signals original work.

---
## Support
If you want, I can tailor the README and demo script to a specific company/domain (finance, healthcare, product docs) to improve shortlisting chances.

---
## Submitted by
**Digvijay** — Final-year student; this submission was prepared as part of a shortlisting assessment. The demo video and README include my personal explanations and design choices.

## Included sample documents and automated tests
- `sample_data/` contains three short, original sample documents (non-copyright) you can ingest immediately to demo the system.
- `tests/run_demo.py` is a small script that ingests those sample docs using the API and runs three queries, saving output into `tests/demo_outputs.json` for reviewers to inspect.
