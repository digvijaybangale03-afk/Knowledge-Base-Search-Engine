# Evaluation checklist (for reviewers)
- [ ] Backend API exists and is reachable.
- [ ] Ingest endpoint handles PDF and plain text.
- [ ] Index (FAISS) is created, persisted to disk.
- [ ] Retrieval returns relevant passages (top-k).
- [ ] LLM synthesis uses retrieved context and cites them.
- [ ] Frontend allows upload + queries and shows answers and sources.
- [ ] Dockerfile and docker-compose present and functioning.
- [ ] README includes deployment and architecture explanations.
- [ ] Demo video script included and saved.

- [ ] Automated demo script (`tests/run_demo.py`) executes using local sample documents.
