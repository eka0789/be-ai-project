import re
from typing import Optional


def clean_text(text: Optional[str]) -> str:
    """
    Clean a text string by replacing null characters and normalizing whitespace.

    Args:
        text: The input text to clean. If None, an empty string is returned.

    Returns:
        Cleaned text with null characters replaced and multiple whitespaces normalized.
    """
    if text is None:
        return ""
    
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text