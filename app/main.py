from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.init_db import init_db
from .routers import upload, evaluate, result


app = FastAPI(
    title="AI CV & Project Evaluator",
    description="API for evaluating CVs and project reports using AI and scoring mechanisms.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database
init_db()


# Include routers
app.include_router(upload.router)
app.include_router(evaluate.router)
app.include_router(result.router)


@app.get("/", response_model=dict)
async def root() -> dict:
    """
    Root endpoint to check if the service is running.

    Returns:
        Dictionary indicating service status and name.
    """
    return {"ok": True, "service": "ai-cv-evaluator"}