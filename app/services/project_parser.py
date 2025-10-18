from typing import Dict
from pypdf import PdfReader
from .text_utils import clean_text


def parse_report(path: str) -> Dict[str, any]:
    """
    Parse a report PDF file to extract text and detect specific sections.

    Args:
        path: Path to the report PDF file.

    Returns:
        Dictionary containing raw text and detected sections.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        Exception: For other errors during PDF processing.
    """
    try:
        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        text = clean_text(" ".join(pages))

        # Detect sections based on predefined keywords
        section_keywords = [
            "prompt", "chaining", "rag", "error", "retry", "testing", "deployment"
        ]
        sections = {
            key: 1 if key.lower() in text.lower() else 0
            for key in section_keywords
        }

        return {
            "raw_text": text,
            "sections": sections,
        }
    except FileNotFoundError:
        raise FileNotFoundError(f"Report file not found: {path}")
    except Exception as e:
        raise Exception(f"Error processing report {path}: {str(e)}")