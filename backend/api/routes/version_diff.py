import json
import os
import re
from difflib import SequenceMatcher
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from groq import Groq
from pydantic import BaseModel, Field

from services.auth_service import get_current_user


load_dotenv()


router = APIRouter(
    prefix="/api/version-diff",
    tags=["Contract Version Diff"],
)


# =========================================================
# CONFIGURATION
# =========================================================

GROQ_MODEL = "openai/gpt-oss-120b"

MAX_COMPARISON_CHARS = 6000
MAX_EXCERPT_CHARS = 900


# =========================================================
# REQUEST MODELS
# =========================================================

class VersionDiffRequest(BaseModel):
    document_a: str = Field(
        ...,
        min_length=20,
        max_length=100000
    )

    document_b: str = Field(
        ...,
        min_length=20,
        max_length=100000
    )

    title_a: str = Field(
        default="Version 1",
        max_length=255
    )

    title_b: str = Field(
        default="Version 2",
        max_length=255
    )


# =========================================================
# RESPONSE MODELS
# =========================================================

class VersionChange(BaseModel):
    section: str
    change_type: str
    version_a: str
    version_b: str
    impact: str


class VersionDiffResponse(BaseModel):
    overall_summary: str
    changes: List[VersionChange]
    key_changes: List[str]
    dates_amounts_changed: List[str]
    review_points: List[str]


# =========================================================
# JSON SCHEMA
# =========================================================

VERSION_DIFF_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "overall_summary": {
            "type": "string"
        },

        "changes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string"
                    },

                    "change_type": {
                        "type": "string",
                        "enum": [
                            "Added",
                            "Removed",
                            "Modified"
                        ]
                    },

                    "version_a": {
                        "type": "string"
                    },

                    "version_b": {
                        "type": "string"
                    },

                    "impact": {
                        "type": "string"
                    }
                },

                "required": [
                    "section",
                    "change_type",
                    "version_a",
                    "version_b",
                    "impact"
                ],

                "additionalProperties": False
            }
        },

        "key_changes": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "dates_amounts_changed": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "review_points": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },

    "required": [
        "overall_summary",
        "changes",
        "key_changes",
        "dates_amounts_changed",
        "review_points"
    ],

    "additionalProperties": False
}


# =========================================================
# HELPER: CLEAN JSON
# =========================================================

def _clean_json_text(text: str) -> str:
    """
    Remove common formatting around JSON returned by the AI.
    """

    if not text:
        raise ValueError(
            "AI returned an empty response."
        )

    cleaned = text.strip()

    # Remove ```json
    cleaned = re.sub(
        r"^```json\s*",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    # Remove ```
    cleaned = re.sub(
        r"^```\s*",
        "",
        cleaned
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned
    )

    return cleaned.strip()


# =========================================================
# HELPER: EXTRACT JSON
# =========================================================

def _extract_json(text: str) -> dict:
    """
    Extract a JSON object from the AI response.

    Handles:
    - normal JSON
    - markdown JSON
    - extra text before JSON
    - extra text after JSON
    """

    cleaned = _clean_json_text(text)

    # -----------------------------------------------------
    # First attempt: entire response is JSON
    # -----------------------------------------------------

    try:
        parsed = json.loads(cleaned)

        if not isinstance(parsed, dict):
            raise ValueError(
                "AI response JSON is not an object."
            )

        return parsed

    except json.JSONDecodeError:
        pass

    # -----------------------------------------------------
    # Second attempt: locate outer JSON object
    # -----------------------------------------------------

    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")

    if first_brace == -1 or last_brace == -1:
        raise ValueError(
            "No JSON object was found in the AI response."
        )

    json_text = cleaned[
        first_brace:last_brace + 1
    ]

    try:
        parsed = json.loads(json_text)

        if not isinstance(parsed, dict):
            raise ValueError(
                "Extracted AI response is not an object."
            )

        return parsed

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"AI returned malformed JSON: {exc}"
        ) from exc


# =========================================================
# HELPER: NORMALIZE LINES
# =========================================================

def _normalise_lines(text: str) -> List[str]:

    text = (
        text
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    return [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]


# =========================================================
# HELPER: TRIM TEXT
# =========================================================

def _trim(
    text: str,
    limit: int = MAX_EXCERPT_CHARS
) -> str:

    text = text.strip()

    if len(text) <= limit:
        return text

    return (
        text[:limit].rstrip()
        + "…"
    )


# =========================================================
# BUILD LOCAL TEXTUAL DIFF
# =========================================================

def _build_change_digest(
    document_a: str,
    document_b: str
) -> str:
    """
    Compare the two documents locally first.

    Only changed sections are sent to Groq.
    """

    lines_a = _normalise_lines(
        document_a
    )

    lines_b = _normalise_lines(
        document_b
    )

    matcher = SequenceMatcher(
        a=lines_a,
        b=lines_b,
        autojunk=False
    )

    packets = []

    for tag, i1, i2, j1, j2 in (
        matcher.get_opcodes()
    ):

        # Ignore identical sections
        if tag == "equal":
            continue

        a_text = "\n".join(
            lines_a[i1:i2]
        )

        b_text = "\n".join(
            lines_b[j1:j2]
        )

        if tag == "replace":
            change_type = "MODIFIED"

        elif tag == "delete":
            change_type = "REMOVED FROM VERSION 1"

        elif tag == "insert":
            change_type = "ADDED IN VERSION 2"

        else:
            change_type = "CHANGED"

        packet = (
            f"[{change_type}]\n"
            f"VERSION 1:\n"
            f"{_trim(a_text)}\n"
            f"VERSION 2:\n"
            f"{_trim(b_text)}"
        )

        packets.append(packet)

    # -----------------------------------------------------
    # No differences
    # -----------------------------------------------------

    if not packets:
        return "NO TEXTUAL DIFFERENCES FOUND."

    separator = (
        "\n\n--- CHANGE ---\n\n"
    )

    digest = separator.join(
        packets
    )

    # -----------------------------------------------------
    # If small enough, send everything
    # -----------------------------------------------------

    if len(digest) <= MAX_COMPARISON_CHARS:
        return digest

    # -----------------------------------------------------
    # Keep only first changed sections
    # -----------------------------------------------------

    kept = []
    total = 0

    for packet in packets:

        extra = len(packet)

        if kept:
            extra += len(separator)

        if (
            total + extra
            > MAX_COMPARISON_CHARS
        ):
            break

        kept.append(packet)
        total += extra

    omitted = (
        len(packets)
        - len(kept)
    )

    result = separator.join(
        kept
    )

    result += (
        "\n\n"
        "[Additional changed sections "
        "omitted from AI prompt: "
        f"{omitted}]"
    )

    return result


# =========================================================
# EXTRACT DATES AND AMOUNTS
# =========================================================

def _extract_date_amount_tokens(
    text: str
) -> List[str]:

    patterns = [

        # 30 days / 12 months / 2 years
        r"\b\d{1,3}\s+"
        r"(?:days?|weeks?|months?|years?)\b",

        # Currency
        r"(?:\$|₹|€|£)\s?"
        r"[\d,]+(?:\.\d+)?",

        # Large numbers
        r"\b\d{1,3}"
        r"(?:,\d{3})+"
        r"(?:\.\d+)?\b",

        # Dates
        r"\b\d{1,2}"
        r"[/-]\d{1,2}"
        r"[/-]\d{2,4}\b",
    ]

    found = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        found.extend(matches)

    # Remove duplicates
    return list(
        dict.fromkeys(found)
    )


# =========================================================
# VALIDATE AI RESULT
# =========================================================

def _validate_result(
    parsed: dict
) -> VersionDiffResponse:

    return VersionDiffResponse.model_validate(
        parsed
    )


# =========================================================
# GROQ CALL
# =========================================================

def _call_groq(
    client: Groq,
    system_prompt: str,
    user_prompt: str
) -> str:

    completion = (
        client.chat.completions.create(
            model=GROQ_MODEL,

            temperature=0.1,

            max_tokens=3000,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            # Ask Groq for JSON.
            response_format={
                "type": "json_object"
            }
        )
    )

    raw = (
        completion
        .choices[0]
        .message
        .content
        or ""
    ).strip()

    return raw


# =========================================================
# REPAIR INVALID JSON
# =========================================================

def _repair_json(
    client: Groq,
    invalid_response: str
) -> str:

    repair_system_prompt = """
You are a JSON repair assistant.

Your task is to convert the supplied malformed AI response
into ONE valid JSON object.

Do not explain anything.

Do not use Markdown.

Do not use ```json.

Return ONLY valid JSON.

The JSON must contain exactly these top-level fields:

overall_summary
changes
key_changes
dates_amounts_changed
review_points

Each item in changes must contain:

section
change_type
version_a
version_b
impact

change_type must be exactly one of:

Added
Removed
Modified

Preserve the information from the supplied response.
Do not invent contract information.
""".strip()

    repair_user_prompt = f"""
MALFORMED AI RESPONSE:

{invalid_response}

Convert it into valid JSON now.
""".strip()

    return _call_groq(
        client,
        repair_system_prompt,
        repair_user_prompt
    )


# =========================================================
# COMPARE VERSIONS API
# =========================================================

@router.post(
    "/compare",
    response_model=VersionDiffResponse
)
def compare_versions(
    payload: VersionDiffRequest,
    current_user=Depends(get_current_user),
):

    # =====================================================
    # CHECK API KEY
    # =====================================================

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:

        raise HTTPException(
            status_code=500,
            detail=(
                "GROQ_API_KEY is not configured."
            )
        )

    # =====================================================
    # BUILD LOCAL DIFF
    # =====================================================

    digest = _build_change_digest(
        payload.document_a,
        payload.document_b
    )

    # =====================================================
    # IDENTICAL DOCUMENTS
    # =====================================================

    if (
        digest
        == "NO TEXTUAL DIFFERENCES FOUND."
    ):

        return VersionDiffResponse(

            overall_summary=(
                "No textual differences were "
                "found between the two supplied "
                "versions."
            ),

            changes=[],

            key_changes=[],

            dates_amounts_changed=[],

            review_points=[]
        )

    # =====================================================
    # DATE / AMOUNT EXTRACTION
    # =====================================================

    date_amount_tokens = (
        _extract_date_amount_tokens(
            payload.document_a
            + "\n"
            + payload.document_b
        )
    )

    date_amount_text = (
        ", ".join(
            date_amount_tokens
        )
        if date_amount_tokens
        else "None detected"
    )

    # =====================================================
    # CREATE GROQ CLIENT
    # =====================================================

    client = Groq(
        api_key=api_key
    )

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = """
You are a contract version comparison assistant.

Compare Version 1 and Version 2 using ONLY
the supplied change digest.

The change digest contains the sections
that differ between the documents.

Do NOT invent information.

Identify meaningful changes involving:

- payment terms
- amounts
- dates
- deadlines
- notice periods
- parties
- obligations
- termination
- liability
- confidentiality
- intellectual property
- dispute resolution
- warranties
- penalties
- renewals
- other important contractual terms

For every change:

1. Identify the section.
2. Classify it as Added, Removed, or Modified.
3. Show the relevant Version 1 wording.
4. Show the relevant Version 2 wording.
5. Explain the practical difference in plain English.

Keep excerpts short.

Do not provide legal advice.

Return ONLY valid JSON.

The JSON must contain:

{
  "overall_summary": "string",
  "changes": [
    {
      "section": "string",
      "change_type": "Added | Removed | Modified",
      "version_a": "string",
      "version_b": "string",
      "impact": "string"
    }
  ],
  "key_changes": ["string"],
  "dates_amounts_changed": ["string"],
  "review_points": ["string"]
}

Do not add any other top-level fields.
""".strip()

    # =====================================================
    # USER PROMPT
    # =====================================================

    user_prompt = f"""
VERSION 1 TITLE:
{payload.title_a}

VERSION 2 TITLE:
{payload.title_b}

CHANGE DIGEST:

{digest}

POTENTIAL DATE / AMOUNT TOKENS:

{date_amount_text}

Compare the changed sections.

Return ONLY valid JSON matching the required structure.
""".strip()

    # =====================================================
    # CALL GROQ
    # =====================================================

    try:

        raw = _call_groq(
            client,
            system_prompt,
            user_prompt
        )

        # -------------------------------------------------
        # DEBUG OUTPUT
        # -------------------------------------------------

        print(
            "\n========== GROQ RAW RESPONSE =========="
        )

        print(raw)

        print(
            "=======================================\n"
        )

        if not raw:

            raise ValueError(
                "The AI returned an empty response."
            )

        # -------------------------------------------------
        # FIRST JSON PARSE
        # -------------------------------------------------

        try:

            parsed = _extract_json(
                raw
            )

            result = _validate_result(
                parsed
            )

            return result

        except Exception as first_error:

            # ---------------------------------------------
            # AI JSON WAS INVALID
            # ---------------------------------------------

            print(
                "\n========== JSON PARSE FAILED =========="
            )

            print(
                str(first_error)
            )

            print(
                "Attempting JSON repair..."
            )

            print(
                "=======================================\n"
            )

            # ---------------------------------------------
            # SECOND AI CALL: REPAIR JSON
            # ---------------------------------------------

            repaired_raw = _repair_json(
                client,
                raw
            )

            print(
                "\n========== GROQ REPAIRED RESPONSE =========="
            )

            print(
                repaired_raw
            )

            print(
                "=============================================\n"
            )

            if not repaired_raw:

                raise ValueError(
                    "AI JSON repair returned an empty response."
                )

            # ---------------------------------------------
            # PARSE REPAIRED JSON
            # ---------------------------------------------

            repaired_parsed = _extract_json(
                repaired_raw
            )

            repaired_result = _validate_result(
                repaired_parsed
            )

            return repaired_result

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except HTTPException:
        raise

    except Exception as exc:

        message = str(exc)

        lower_message = (
            message.lower()
        )

        # -------------------------------------------------
        # RATE LIMIT / LARGE REQUEST
        # -------------------------------------------------

        if (
            "request too large"
            in lower_message

            or "tokens per minute"
            in lower_message

            or "rate_limit_exceeded"
            in lower_message

            or "413"
            in lower_message
        ):

            raise HTTPException(
                status_code=413,
                detail=(
                    "The contract versions are too "
                    "large for the current AI request "
                    "limit. The system already sends "
                    "only changed sections. Try "
                    "shorter contract versions or "
                    "smaller files."
                )
            )

        # -------------------------------------------------
        # JSON / STRUCTURED OUTPUT ERROR
        # -------------------------------------------------

        if (
            "json" in lower_message

            or "delimiter" in lower_message

            or "schema" in lower_message

            or "validation" in lower_message
        ):

            raise HTTPException(
                status_code=500,
                detail=(
                    "The AI returned an invalid "
                    "comparison result. The system "
                    "attempted to repair the response. "
                    "Please try comparing the versions "
                    "again."
                )
            )

        # -------------------------------------------------
        # GENERIC ERROR
        # -------------------------------------------------

        raise HTTPException(
            status_code=500,
            detail=(
                f"Version comparison failed: "
                f"{message}"
            )
        )