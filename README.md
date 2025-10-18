# AI CV & Project Evaluator — FastAPI + Celery + ChromaDB
-H 'Content-Type: application/json' \
-d '{"job_title":"Backend Engineer","cv_id":"cv_xxx","report_id":"report_xxx"}'
```
- Check result:
```bash
curl http://localhost:8000/result/job_xxxx
```


### Example Completed Response
```json
{
"id": "job_ab12cd34",
"status": "completed",
"result": {
"cv_match_rate": 0.84,
"cv_detail": {"technical":4,"experience":4,"achievements":3,"culture":4},
"cv_feedback": "Strong backend exposure; deepen LLM/RAG production experience.",
"project_score": 4.5,
"project_detail": {"correctness":5,"code_quality":5,"resilience":5,"docs":5,"creativity":5},
"project_feedback": "Meets prompt/chaining/RAG; improve testing depth and failure-mode handling.",
"overall_summary": "Solid profile; aligns with backend + AI needs; recommended for next round."
}
}
```


---


## LLM & RAG Notes
- **Embeddings**: offline via `SentenceTransformer all-MiniLM-L6-v2` → consistent tests
- **LLM feedback**: If `OPENAI_API_KEY` present → real model `OPENAI_MODEL` used. Else → heuristic strings (deterministic)
- **Retrieval**: 3 nearest chunks per collection (JD / Brief / Rubrics) injected into prompts
- **Randomness Control**: `temperature=0.2`, retries/backoff (Celery `autoretry_for`, `retry_backoff`), time limits


---


## Testing
```bash
pytest -q
```
- `tests/test_scoring.py` covers weighted scoring
- `tests/test_api.py` covers root, upload, evaluate enqueuing (monkeypatched)


> For full E2E, run a worker & Redis, then call API from Postman; include screenshots in your submission per brief.


---


## Design Choices & Trade-offs
- **Offline-first** to guarantee zero external dependency for reviewers; OpenAI optional for richer feedback
- **ChromaDB local** keeps setup simple; can swap to Qdrant/pgvector later
- **SQLite** is sufficient for job/doc metadata; easy to move to Postgres
- **Celery + Redis** are common, battle-tested for long-running jobs and retries
- **Parsing** uses `pypdf` for simplicity; could swap to `pdfminer.six` for tougher PDFs
- **Security**: This is a demo service; add auth (JWT), file size/type limits, and S3 for production


---


## Edge Cases Considered
- Corrupted PDFs → parser errors → job status `failed` with message
- Empty internal store → RAG returns empty context → heuristics still produce output
- LLM API timeouts → Celery retries with exponential backoff; soft/hard time limits
- Nonexistent doc IDs → 404


---


## Submission Checklist (per brief)
- [x] Endpoints: `/upload`, `/evaluate`, `/result/{id}`
- [x] Async long-running process
- [x] RAG ingestion & retrieval
- [x] Prompt design & chaining (via `llm_client` + contexts)
- [x] Scoring aligned to rubric (weights documented)
- [x] Error handling & retries
- [x] README with run instructions & design choices
- [x] Unit tests


---


## License
MIT