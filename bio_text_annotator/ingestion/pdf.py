from pathlib import Path

import fitz


def extract_text(pdf_path: str | Path) -> str:
    """
    Extract raw text from a PDF document.

    Args:
        pdf_path: Path to PDF file.

    Returns:
        Extracted document text as a single string.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    text_parts = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text()

            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)