"""Utilities for extracting readable text from job posting HTML."""

import trafilatura
from enum import StrEnum


class ExtractionStatus(StrEnum):
    """Represent extracted text quality."""

    USABLE = "usable"
    WEAK = "weak"
    FAILED = "failed"


def extract_text_from_html(html: str, url: str = "") -> str:
    """Extract readable text from raw HTML."""

    text = trafilatura.extract(
        html,
        url=url or None,
        include_comments=False,
        include_tables=False,
    )

    if not text:
        return ""

    # removes whitespace from the beginning and end of the string.
    return text.strip()


MIN_USABLE_TEXT_LENGTH = 2000
MIN_WEAK_TEXT_LENGTH = 500


def evaluate_extracted_text(text: str) -> ExtractionStatus:
    """Return the quality status of extracted job-posting text."""

    text_length = len(text.strip())

    if text_length < MIN_WEAK_TEXT_LENGTH:
        return ExtractionStatus.FAILED

    if text_length < MIN_USABLE_TEXT_LENGTH:
        return ExtractionStatus.WEAK

    return ExtractionStatus.USABLE