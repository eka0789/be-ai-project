import os
from typing import List
from pypdf import PdfReader
from .vector_store import COLLECTIONS
from ..utils.config import get_settings

# Initialize settings and directories
settings = get_settings()
INTERNAL_DIR = os.path.join(settings.STORAGE_DIR, "internal")

# Define files to ingest into ChromaDB collections
FILES = {
    "job_desc": ["job_description.pdf"],
    "case_brief": ["case_study_brief.pdf"],
    "cv_rubric": ["cv_scoring_rubric.pdf"],
    "project_rubric": ["project_scoring_rubric.pdf"],
}


def _pdf_to_pages(path: str) -> List[str]:
    """
    Extract text from each page of a PDF file.

    Args:
        path: Path to the PDF file.

    Returns:
        List of extracted text from each page.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        Exception: For other errors during PDF processing.
    """
    text_pages = []
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            text = page.extract_text() or ""
            text_pages.append(text)
        return text_pages
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found: {path}")
    except Exception as e:
        raise Exception(f"Error processing PDF {path}: {str(e)}")


def ingest() -> None:
    """
    Ingest PDF files into ChromaDB collections.

    For each file in FILES, extract text from PDF pages and upsert into the corresponding
    ChromaDB collection with unique IDs and metadata.
    """
    for col_name, files in FILES.items():
        col = COLLECTIONS.get(col_name)
        if not col:
            print(f"[ERROR] Collection {col_name} not found in COLLECTIONS")
            continue

        for fname in files:
            fpath = os.path.join(INTERNAL_DIR, fname)
            if not os.path.exists(fpath):
                print(f"[WARNING] Missing internal file: {fpath}")
                continue

            try:
                pages = _pdf_to_pages(fpath)
                ids = [f"{fname}-{i}" for i in range(len(pages))]
                metadatas = [{"source": fname, "page": i} for i in range(len(pages))]
                col.upsert(ids=ids, documents=pages, metadatas=metadatas)
                print(f"[INFO] Ingested {len(pages)} pages from {fname} into {col_name}")
            except Exception as e:
                print(f"[ERROR] Failed to ingest {fname}: {str(e)}")


if __name__ == "__main__":
    ingest()