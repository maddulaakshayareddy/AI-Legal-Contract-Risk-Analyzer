from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""

    try:
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        result = "\n\n".join(pages).strip()

        if not result:
            raise ValueError(
                "The PDF does not contain readable text."
            )

        return result

    except Exception as exc:
        raise ValueError(
            f"Unable to read PDF file: {exc}"
        )


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""

    try:
        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        # Also read text from tables
        for table in document.tables:
            for row in table.rows:
                row_text = []

                for cell in row.cells:
                    cell_text = cell.text.strip()

                    if cell_text:
                        row_text.append(cell_text)

                if row_text:
                    paragraphs.append(" | ".join(row_text))

        result = "\n\n".join(paragraphs).strip()

        if not result:
            raise ValueError(
                "The DOCX file does not contain readable text."
            )

        return result

    except Exception as exc:
        raise ValueError(
            f"Unable to read DOCX file: {exc}"
        )


def extract_contract_text(file_path: str) -> str:
    """Extract contract text based on file extension."""

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. "
            "Only PDF and DOCX files are supported."
        )

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError("Unsupported document type.")