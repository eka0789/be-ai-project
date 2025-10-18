# AI CV & Project Evaluator — FastAPI + Celery + ChromaDB

This service evaluates candidate CVs and project submissions asynchronously using FastAPI, Celery, and ChromaDB.

## API Endpoints

### Submit Evaluation
Use the following command to submit an evaluation:
```bash
curl -H 'Content-Type: application/json' \
-d '{"job_title":"Backend Engineer","cv_id":"cv_xxx","report_id":"report_xxx"}' \
http://localhost:8000/evaluate
```

### Check Result
Retrieve the evaluation result:
```bash
curl http://localhost:8000/result/job_xxxx
```

### Example Response
```json
{
    "id": "job_ab12cd34",
    "status": "completed",
    "result": {
        "cv_match_rate": 0.84,
        "cv_detail": {
            "technical": 4,
            "experience": 4,
            "achievements": 3,
            "culture": 4
        },
        "cv_feedback": "Strong backend exposure; deepen LLM/RAG production experience.",
        "project_score": 4.5,
        "project_detail": {
            "correctness": 5,
            "code_quality": 5,
            "resilience": 5,
            "docs": 5,
            "creativity": 5
        },
        "project_feedback": "Meets prompt/chaining/RAG; improve testing depth and failure-mode handling.",
        "overall_summary": "Solid profile; aligns with backend + AI needs; recommended for next round."
    }
}
```

## LLM & RAG Details
- **Embeddings**: Generated offline using `SentenceTransformer all-MiniLM-L6-v2` for consistent testing.
- **LLM Feedback**: If an `OPENAI_API_KEY` is provided, the specified `OPENAI_MODEL` is used; otherwise, deterministic heuristic strings are produced.
- **Retrieval**: Injects the three nearest chunks per collection (Job Description, Brief, Rubrics) into prompts.
- **Randomness Control**: Configured with `temperature=0.2` and employs retries with exponential backoff via Celery.

## Testing
Run the tests with:
```bash
pytest -q
```
- `tests/test_scoring.py`: Validates weighted scoring.
- `tests/test_api.py`: Tests endpoints including root, upload, and evaluation enqueuing (monkeypatched).

For a full end-to-end test, run a worker and Redis, then call the API from Postman. Include screenshots in your submission as required.

## Design Choices & Trade-offs
- **Offline-first Approach**: Eliminates external dependencies for reviewers; OpenAI is optional for richer feedback.
- **Local ChromaDB**: Simplifies setup and can later be swapped with Qdrant or pgvector.
- **SQLite**: Suitable for job/document metadata with easy migration to PostgreSQL if needed.
- **Celery + Redis**: Provides robust handling for long-running jobs and retries.
- **PDF Parsing**: Uses `pypdf` for simplicity; switch to `pdfminer.six` for more challenging PDFs.
- **Security Considerations**: As a demo service, advanced features like JWT auth, file size/type limits, and S3 integration are recommended for production.

## Edge Cases
- **Corrupted PDFs**: Parser errors mark the job as `failed` with an error message.
- **Empty Internal Store**: If no context is available, heuristic methods still generate output.
- **LLM API Timeouts**: Handled by Celery with retries and defined time limits.
- **Invalid Document IDs**: Returns a 404 error.

## Submission Checklist
- [x] API Endpoints: `/upload`, `/evaluate`, `/result/{id}`
- [x] Asynchronous process handling
- [x] RAG ingestion & retrieval
- [x] Prompt chaining using `llm_client` and context injections
- [x] Scoring aligned with documented rubrics
- [x] Robust error handling & retries
- [x] Detailed README with installation, run instructions, and design rationale
- [x] Comprehensive unit tests

## License
MIT
