from typing import List
from . import text_utils
from ..db.vector_store import COLLECTIONS


def retrieve_context(kind: str, query: str, k: int = 3) -> List[str]:
    """
    Retrieve relevant context from a ChromaDB collection based on the query.

    Args:
        kind: The name of the collection to query (e.g., "job_desc", "case_brief").
        query: The query text to search for.
        k: Number of results to retrieve (default: 3).

    Returns:
        List of cleaned text documents retrieved from the collection.

    Raises:
        KeyError: If the specified collection kind is not found in COLLECTIONS.
        Exception: For errors during the query process.
    """
    if kind not in COLLECTIONS:
        raise KeyError(f"Collection '{kind}' not found in COLLECTIONS")

    col = COLLECTIONS[kind]
    try:
        result = col.query(query_texts=[query], n_results=k)
        docs = result.get("documents", [[]])[0]
        return [text_utils.clean_text(doc) for doc in docs if doc]
    except Exception as e:
        raise Exception(f"Error querying collection '{kind}': {str(e)}")