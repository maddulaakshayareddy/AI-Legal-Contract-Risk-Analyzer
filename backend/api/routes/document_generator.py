from io import BytesIO
import html
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from groq import Groq
from pydantic import BaseModel, Field

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from services.auth_service import get_current_user


router = APIRouter(
    prefix="/api/document-generator",
    tags=["Document Generator"],
)


SUPPORTED_DOCUMENT_LANGUAGES = {
    "Assamese",
    "Bengali",
    "Bodo",
    "Dogri",
    "Gujarati",
    "Hindi",
    "Kannada",
    "Kashmiri",
    "Konkani",
    "Maithili",
    "Malayalam",
    "Manipuri",
    "Marathi",
    "Nepali",
    "Odia",
    "Punjabi",
    "Sanskrit",
    "Santali",
    "Sindhi",
    "Tamil",
    "Telugu",
    "Urdu",
    "English",
    "Spanish",
    "French",
    "German",
    "Arabic",
    "Bhojpuri",
    "Rajasthani",
    "Tulu",
    "Awadhi",
    "Magahi",
    "Chhattisgarhi",
    "Haryanvi",
    "Marwari",
    "Garhwali",
    "Kumaoni",
    "Bundeli",
    "Mewari",
}


class DocumentGenerateRequest(BaseModel):
    document_type: str = Field(
        min_length=2,
        max_length=100
    )

    details: str = Field(
        min_length=10,
        max_length=10000
    )

    document_language: str = Field(
        default="English",
        min_length=2,
        max_length=50
    )


def get_language_instruction(document_language: str) -> str:
    """
    Return strict language instructions for the selected language.
    """

    return f"""
The requested output language is: {document_language}

LANGUAGE REQUIREMENTS:

1. Write the ENTIRE document in {document_language}.
2. Do not switch to English unless the selected language is English.
3. Do not translate only the headings. The complete document must use
   {document_language}.
4. Do not transliterate {document_language} into English/Roman letters.
5. Use natural, grammatically correct and professional {document_language}.
6. Keep legal and business terminology appropriate for {document_language}.
7. Do not generate meaningless words, random syllables, repeated characters,
   corrupted words, or invented language.
8. Do not repeat the same sentence, paragraph, clause, or section.
9. Every numbered clause must contain meaningful information.
10. Stop after the document is complete. Do not continue generating filler.
"""


def generate_document_content(
    document_type: str,
    details: str,
    document_language: str,
) -> str:

    if document_language not in SUPPORTED_DOCUMENT_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported document language: {document_language}",
        )

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Groq API configuration is missing.",
        )

    try:
        client = Groq(api_key=api_key)

        language_instruction = get_language_instruction(
            document_language
        )

        prompt = f"""
You are LegalLens AI, a professional legal and business
document drafting assistant.

Create a complete, practical first draft of the requested document.

DOCUMENT TYPE:
{document_type}

SELECTED DOCUMENT LANGUAGE:
{document_language}

USER REQUIREMENTS:
{details}

{language_instruction}

DOCUMENT STRUCTURE:

Use a sensible structure for the requested document.

For a business or legal agreement, use sections such as:

1. Title
2. Parties
3. Purpose
4. Scope of Agreement
5. Responsibilities / Obligations
6. Payment / Commercial Terms
7. Confidentiality
8. Intellectual Property
9. Term and Termination
10. Liability
11. Dispute Resolution
12. Governing Law
13. Miscellaneous
14. Signatures

Only include sections that are relevant to the requested document.

CONTENT RULES:

- Preserve the meaning of the user's requirements.
- Do not invent personal information.
- Do not invent real company names.
- Use placeholders such as [Company Name], [Date],
  [Address], [Amount] when information is missing.
- Do not make unsupported factual claims.
- Do not add legal advice outside the document.
- Do not mention that an AI generated the document.
- Do not include an explanation before or after the document.
- Return ONLY the document.

QUALITY CONTROL:

Before returning the document, internally check that:

- The language is {document_language}.
- The document is coherent from beginning to end.
- No section is duplicated.
- No sentence is repeated.
- No meaningless repeated words or syllables appear.
- No random Roman-character transliteration is used for Indian-language text.
- The document ends naturally.
- There is no unfinished sentence or unfinished clause.

Return only the final document.
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are LegalLens AI, a professional multilingual "
                        "legal and business document drafting assistant. "
                        "Produce coherent, non-repetitive documents. "
                        "Never output meaningless repeated text."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.1,
            max_tokens=5000,
        )

        content = response.choices[0].message.content

        if not content:
            raise HTTPException(
                status_code=500,
                detail="No document content was generated.",
            )

        content = content.strip()

        if len(content) < 50:
            raise HTTPException(
                status_code=500,
                detail="The generated document is too short.",
            )

        return content

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {str(exc)}",
        ) from exc


@router.post("/generate")
def generate_document(
    payload: DocumentGenerateRequest,
    current_user=Depends(get_current_user),
):
    content = generate_document_content(
        document_type=payload.document_type,
        details=payload.details,
        document_language=payload.document_language,
    )

    return {
        "document_type": payload.document_type,
        "document_language": payload.document_language,
        "content": content,
    }


@router.post("/generate-pdf")
def generate_document_pdf(
    payload: DocumentGenerateRequest,
    current_user=Depends(get_current_user),
):
    content = generate_document_content(
        document_type=payload.document_type,
        details=payload.details,
        document_language=payload.document_language,
    )

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=payload.document_type,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocumentTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=22,
        spaceAfter=14,
    )

    language_style = ParagraphStyle(
        "LanguageInfo",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=9,
        leading=12,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "DocumentHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "DocumentBody",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=16,
        spaceAfter=7,
    )

    story = []

    story.append(
        Paragraph(
            html.escape(payload.document_type),
            title_style,
        )
    )

    story.append(
        Paragraph(
            html.escape(
                f"Language: {payload.document_language}"
            ),
            language_style,
        )
    )

    lines = content.splitlines()

    for line in lines:

        cleaned = line.strip()

        if not cleaned:
            story.append(
                Spacer(1, 5)
            )
            continue

        if cleaned.startswith("#"):

            heading_text = cleaned.lstrip("#").strip()

            heading_text = (
                heading_text
                .replace("**", "")
                .replace("__", "")
            )

            story.append(
                Paragraph(
                    html.escape(heading_text),
                    heading_style,
                )
            )

        else:

            cleaned = (
                cleaned
                .replace("**", "")
                .replace("__", "")
            )

            story.append(
                Paragraph(
                    html.escape(cleaned),
                    body_style,
                )
            )

    document.build(story)

    pdf_buffer.seek(0)

    safe_name = (
        payload.document_type
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    safe_language = (
        payload.document_language
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; '
                f'filename="{safe_name}_{safe_language}.pdf"'
            )
        },
    )