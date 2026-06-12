import re
import unicodedata
from pathlib import Path
import fitz  # PyMuPDF


# XML / PDF junk
_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")
_REPLACEMENT_CHAR_RE = re.compile(r"\uFFFD")

# Whitespace
_MULTISPACE_RE = re.compile(r"[ \t]+")
_MULTINEWLINE_RE = re.compile(r"\n{3,}")

# PDF hyphenation:
# interac-\ntion -> interaction
_HYPHEN_BREAK_RE = re.compile(r"([A-Za-z])-\s*\n\s*([A-Za-z])")

# Unicode hyphen variants
_UNICODE_HYPHEN_BREAK_RE = re.compile(
    r"([A-Za-z])[\-\u2010\u2011\u2012\u2013\u2014]\s*\n\s*([A-Za-z])"
)

# Soft / zero-width chars
_SOFT_NOISE_RE = re.compile(r"[\u00AD\u200B\u200C\u200D\uFEFF]")

# HGVS normalization
#
# c.233A > G -> c.233A>G
# c.394C > T -> c.394C>T
#
_HGVS_SUBSTITUTION_RE = re.compile(r"([cgm]\.\d+[A-Za-z*]+)\s*>\s*([A-Za-z*]+)")

#
# p.Val74Leufs * 85 -> p.Val74Leufs*85
#
_HGVS_STAR_RE = re.compile(r"([A-Za-z0-9]+)\s+\*\s*(\d+)")


def sanitize_for_tmvar(text: str) -> str:
    """
    Normalize PDF text for TMVar.

    Keeps biomedical notation intact:
    - HGVS variants
    - mutation punctuation
    - sentence boundaries
    """

    # Unicode normalization
    text = unicodedata.normalize("NFC", text)

    # Remove invisible PDF artifacts
    text = _SOFT_NOISE_RE.sub("", text)
    text = _REPLACEMENT_CHAR_RE.sub("", text)
    text = _CONTROL_CHARS_RE.sub("", text)

    # Fix PDF line wrapping
    text = _UNICODE_HYPHEN_BREAK_RE.sub(r"\1\2", text)
    text = _HYPHEN_BREAK_RE.sub(r"\1\2", text)

    # Normalize HGVS spacing BEFORE general whitespace cleanup
    text = _HGVS_SUBSTITUTION_RE.sub(r"\1>\2", text)
    text = _HGVS_STAR_RE.sub(r"\1*\2", text)

    # Normalize spaces but preserve newlines
    text = _MULTISPACE_RE.sub(" ", text)

    # Prevent huge blank regions
    text = _MULTINEWLINE_RE.sub("\n\n", text)

    # Strip line endings
    text = "\n".join(line.rstrip() for line in text.splitlines())

    return text.strip()


def extract_text(pdf_path: str | Path) -> str:
    """
    Extract PDF text with minimal layout disruption.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages: list[str] = []

    with fitz.open(pdf_path) as doc:
        for page in doc:

            raw = page.get_text("text", sort=True, flags=fitz.TEXT_PRESERVE_WHITESPACE)

            if raw:
                pages.append(raw)

    combined = "\n".join(pages)

    return sanitize_for_tmvar(combined)
