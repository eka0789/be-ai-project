import os
import chromadb
from chromadb.utils import embedding_functions
from ..utils.config import get_settings

# Initialize settings
settings = get_settings()

# Ensure ChromaDB storage directory exists
os.makedirs(settings.CHROMA_DIR, exist_ok=True)

# Initialize ChromaDB persistent client
client = chromadb.PersistentClient(path=settings.CHROMA_DIR)

# Configure embedding function (SentenceTransformer for offline use)
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=settings.EMBEDDING_MODEL
)

# Define collections for ChromaDB
COLLECTIONS = {
    "job_desc": client.get_or_create_collection(
        name="job_desc",
        embedding_function=embed_fn,
    ),
    "case_brief": client.get_or_create_collection(
        name="case_brief",
        embedding_function=embed_fn,
    ),
    "cv_rubric": client.get_or_create_collection(
        name="cv_rubric",
        embedding_function=embed_fn,
    ),
    "project_rubric": client.get_or_create_collection(
        name="project_rubric",
        embedding_function=embed_fn,
    ),
}