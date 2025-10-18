import re
from typing import Dict
from pypdf import PdfReader
from .text_utils import clean_text


SKILL_KEYWORDS = [
    "python", "fastapi", "django", "flask", "node", "express", "java", "ruby", "rails",
    "postgres", "mysql", "mongodb", "redis", "rabbitmq", "kafka", "docker", "kubernetes",
    "aws", "gcp", "azure", "rest", "grpc", "graphql", "celery", "llm", "rag", "prompt",
]


def parse_cv(path: str) -> Dict[str, any]:
    """
    Parse a CV PDF file to extract text, skills, and years of experience.

    Args:
        path: Path to the CV PDF file.

    Returns:
        Dictionary containing raw text, detected skills, and years of experience.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        Exception: For other errors during PDF processing.
    """
    try:
        reader = PdfReader(path)
        text = " ".join([page.extract_text() or "" for page in reader.pages])
        text = clean_text(text)

        # Detect skills from predefined keywords
        found_skills = {
            keyword: 1 if keyword.lower() in text.lower() else 0
            for keyword in SKILL_KEYWORDS
        }

        # Extract years of experience (naive approach)
        years = 0
        match = re.search(r"(\d+)\+?\s*(years|yrs|tahun)", text, re.IGNORECASE)
        if match:
            years = int(match.group(1))

        return {
            "raw_text": text,
            "skills": found_skills,
            "years": years,
        }
    except FileNotFoundError:
        raise FileNotFoundError(f"CV file not found: {path}")
    except Exception as e:
        raise Exception(f"Error processing CV {path}: {str(e)}")