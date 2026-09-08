"""Extracts plain text from an uploaded resume file.

In the real job market, resumes almost never arrive as plain text --
they're PDFs (LinkedIn/Canva/Google Docs exports) or DOCX files. This is
the one place that turns those formats into the plain text the rest of
the pipeline (`compare_resume_jd`) already expects.

This is a request-layer utility, not an ADK tool: the LLM never decides
to call it -- the web/CLI layer runs it once, up front, on a file the
user picked, then hands the resulting text to the agent like any other
message.
"""

from io import BytesIO
from pathlib import Path

from docx import Document
from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def extract_resume_text(data: bytes, filename: str) -> str:
    """Extract plain text from a resume file (.pdf, .docx, .txt, .md).

    Raises ValueError with a user-facing message for an oversized file,
    an unsupported type, or a file with no extractable text (e.g. a
    scanned image PDF with no text layer).
    """
    if len(data) > MAX_FILE_SIZE_BYTES:
        raise ValueError("File too large (max 5 MB).")

    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext or 'unknown'}'. "
            "Upload a PDF, DOCX, or plain text resume."
        )

    if ext == ".pdf":
        text = _extract_pdf(data)
    elif ext == ".docx":
        text = _extract_docx(data)
    else:
        text = data.decode("utf-8", errors="ignore")

    text = _normalize_whitespace(text)
    if not text:
        raise ValueError(
            "Could not extract any text from this file. It may be a "
            "scanned image without a text layer -- try pasting the "
            "resume text directly instead."
        )
    return text


def _extract_pdf(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _extract_docx(data: bytes) -> str:
    document = Document(BytesIO(data))
    return "\n".join(p.text for p in document.paragraphs)


def _normalize_whitespace(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)
