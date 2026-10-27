import json
import os
import re
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from groq import Groq
from pydantic import BaseModel, Field

from services.auth_service import get_current_user


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

router = APIRouter(
    prefix="/api/obligations",
    tags=["Dates & Obligations"]
)

GROQ_MODEL = "openai/gpt-oss-120b"

MAX_SOURCE_CHARS = 9000
MAX_OBLIGATIONS = 20
MAX_DATES = 15
MAX_RENEWAL_ALERTS = 10


# =========================================================
# REQUEST MODEL
# =========================================================

class ObligationRequest(BaseModel):
    contract_text: str = Field(
        ...,
        min_length=20,
        max_length=100000
    )


# =========================================================
# RESPONSE MODELS
# =========================================================

class ImportantDate(BaseModel):
    label: str
    value: str
    source: str
    notes: str = ""


class ContractObligation(BaseModel):
    obligation_type: str
    requirement: str
    deadline: str
    responsible_party: str
    source: str
    notes: str = ""


class ObligationsResponse(BaseModel):
    important_dates: List[ImportantDate]
    obligations: List[ContractObligation]
    renewal_alerts: List[str]
    general_notes: List[str]


# =========================================================
# JSON EXTRACTION
# =========================================================

def _extract_json(text: str):
    """
    Safely extract a JSON object from an AI response.
    Handles:
    - normal JSON
    - ```json ... ```
    - extra text around JSON
    - trailing commas
    """

    cleaned = (text or "").strip()

    if not cleaned:
        raise ValueError(
            "The AI returned an empty response."
        )

    # Remove markdown code fences.
    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned
    )

    # First attempt: entire response.
    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        pass

    # Find first JSON object.
    start = cleaned.find("{")

    if start == -1:
        raise ValueError(
            "The AI response did not contain a JSON object."
        )

    depth = 0
    in_string = False
    escaped = False
    end = None

    for index in range(
        start,
        len(cleaned)
    ):

        char = cleaned[index]

        if in_string:

            if escaped:
                escaped = False

            elif char == "\\":
                escaped = True

            elif char == '"':
                in_string = False

            continue

        if char == '"':
            in_string = True

        elif char == "{":
            depth += 1

        elif char == "}":
            depth -= 1

            if depth == 0:
                end = index + 1
                break

    if end is None:
        raise ValueError(
            "The AI response contained an incomplete JSON object."
        )

    candidate = cleaned[
        start:end
    ]

    try:
        return json.loads(candidate)

    except json.JSONDecodeError as exc:

        # Remove trailing commas.
        repaired = re.sub(
            r",\s*([}\]])",
            r"\1",
            candidate
        )

        try:
            return json.loads(repaired)

        except json.JSONDecodeError:

            raise ValueError(
                f"The AI returned malformed JSON: {exc}"
            ) from exc


# =========================================================
# RESPONSIBLE PARTY DETECTION
# =========================================================

def _detect_responsible_party(
    text: str
) -> str:

    if not text:
        return "Not specified"

    text_clean = text.strip()

    # -----------------------------------------------------
    # Direct party names
    # -----------------------------------------------------

    party_patterns = [
        (
            r"\b(?:the\s+)?client\b"
            r"(?=\s+(?:shall|must|will|required|is|agrees|"
            r"may|has|will be|is responsible))",
            "Client"
        ),

        (
            r"\b(?:the\s+)?provider\b"
            r"(?=\s+(?:shall|must|will|required|is|agrees|"
            r"may|has|will be|is responsible))",
            "Provider"
        ),

        (
            r"\b(?:the\s+)?vendor\b"
            r"(?=\s+(?:shall|must|will|required|is|agrees|"
            r"may|has|will be|is responsible))",
            "Vendor"
        ),

        (
            r"\b(?:the\s+)?customer\b"
            r"(?=\s+(?:shall|must|will|required|is|agrees|"
            r"may|has|will be|is responsible))",
            "Customer"
        ),

        (
            r"\b(?:the\s+)?seller\b"
            r"(?=\s+(?:shall|must|will|required|is|agrees|"
            r"may|has|will be|is responsible))",
            "Seller"
        ),

        (
            r"\b(?:the\s+)?buyer\b"
            r"(?=\s+(?:shall|must|will|required|is|agrees|"
            r"may|has|will be|is responsible))",
            "Buyer"
        ),
    ]

    for pattern, party in party_patterns:

        if re.search(
            pattern,
            text_clean,
            flags=re.IGNORECASE
        ):
            return party

    # -----------------------------------------------------
    # "Each party"
    # -----------------------------------------------------

    if re.search(
        r"\beach\s+party\b",
        text_clean,
        flags=re.IGNORECASE
    ):
        return "Both parties"

    # -----------------------------------------------------
    # "Either party"
    # -----------------------------------------------------

    if re.search(
        r"\beither\s+party\b",
        text_clean,
        flags=re.IGNORECASE
    ):
        return "Either party"

    # -----------------------------------------------------
    # "Parties"
    # -----------------------------------------------------

    if re.search(
        r"\bthe\s+parties\b",
        text_clean,
        flags=re.IGNORECASE
    ):
        return "Both parties"

    # -----------------------------------------------------
    # Common subject before shall/must/will
    # -----------------------------------------------------

    subject_match = re.search(
        r"^\s*([A-Z][A-Za-z0-9 .,&()'-]{1,80}?)"
        r"\s+(?:shall|must|will|required to|agrees to)\b",
        text_clean
    )

    if subject_match:

        subject = (
            subject_match
            .group(1)
            .strip()
        )

        if len(subject) <= 80:
            return subject

    return "Not specified"


# =========================================================
# OBLIGATION TYPE DETECTION
# =========================================================

def _detect_obligation_type(
    text: str
) -> str:

    lower = text.lower()

    if any(
        word in lower
        for word in (
            "payment",
            "pay",
            "invoice",
            "fee",
            "fees",
            "interest",
            "reimburse",
            "reimbursement",
            "amount due",
            "payable"
        )
    ):
        return "Payment"

    if any(
        word in lower
        for word in (
            "deliver",
            "delivery",
            "provide",
            "provided",
            "services",
            "software",
            "goods"
        )
    ):
        return "Delivery"

    if any(
        word in lower
        for word in (
            "notice",
            "notify",
            "notification",
            "written notice"
        )
    ):
        return "Notice"

    if any(
        word in lower
        for word in (
            "report",
            "reporting",
            "report to"
        )
    ):
        return "Reporting"

    if any(
        word in lower
        for word in (
            "renew",
            "renewal",
            "automatically renew",
            "extension"
        )
    ):
        return "Renewal"

    if any(
        word in lower
        for word in (
            "terminate",
            "termination",
            "termination notice"
        )
    ):
        return "Termination"

    if any(
        word in lower
        for word in (
            "confidential",
            "confidentiality",
            "non-disclosure"
        )
    ):
        return "Confidentiality"

    if any(
        word in lower
        for word in (
            "indemnify",
            "indemnification",
            "hold harmless"
        )
    ):
        return "Indemnification"

    if any(
        word in lower
        for word in (
            "intellectual property",
            "copyright",
            "ownership",
            "license",
            "licence"
        )
    ):
        return "Intellectual Property"

    if any(
        word in lower
        for word in (
            "data protection",
            "security",
            "personal data",
            "data breach",
            "cybersecurity"
        )
    ):
        return "Data Protection"

    if any(
        word in lower
        for word in (
            "audit",
            "audit rights",
            "records"
        )
    ):
        return "Audit"

    return "Other"


# =========================================================
# DEADLINE DETECTION
# =========================================================

def _detect_deadline(
    text: str
) -> str:

    lower = text.lower()

    # -----------------------------------------------------
    # within / in X days
    # -----------------------------------------------------

    match = re.search(
        r"\b(?:within|in)\s+"
        r"(\d+)\s+"
        r"(day|days|week|weeks|month|months|year|years)\b",
        lower
    )

    if match:

        return (
            f"{match.group(1)} "
            f"{match.group(2)}"
        )

    # -----------------------------------------------------
    # X days notice
    # -----------------------------------------------------

    match = re.search(
        r"\b(\d+)\s+"
        r"(day|days|week|weeks|month|months|year|years)"
        r"\s+(?:prior\s+)?notice\b",
        lower
    )

    if match:

        return (
            f"{match.group(1)} "
            f"{match.group(2)} notice"
        )

    # -----------------------------------------------------
    # X days after / before
    # -----------------------------------------------------

    match = re.search(
        r"\b(\d+)\s+"
        r"(day|days|week|weeks|month|months|year|years)"
        r"\s+(?:after|before)\b",
        lower
    )

    if match:

        return (
            f"{match.group(1)} "
            f"{match.group(2)} "
            f"{re.search(r'(after|before)', match.group(0)).group(1)}"
        )

    # -----------------------------------------------------
    # Calendar date
    # -----------------------------------------------------

    date_match = re.search(
        r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|"
        r"apr(?:il)?|may|jun(?:e)?|jul(?:y)?|"
        r"aug(?:ust)?|sep(?:t(?:ember)?)?|"
        r"oct(?:ober)?|nov(?:ember)?|"
        r"dec(?:ember)?)\s+"
        r"\d{1,2}(?:st|nd|rd|th)?"
        r"(?:,\s*\d{4})?\b",
        text,
        flags=re.IGNORECASE
    )

    if date_match:
        return date_match.group(0)

    # Numeric date
    numeric_date = re.search(
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        text
    )

    if numeric_date:
        return numeric_date.group(0)

    return "Not specified"


# =========================================================
# CANDIDATE LINE EXTRACTION
# =========================================================

def _candidate_lines(
    text: str
) -> str:

    normalized = (
        text
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    lines = [
        line.strip()
        for line in normalized.split("\n")
        if line.strip()
    ]

    keywords = (
        "effective",
        "commencement",
        "start date",
        "execution",
        "entered into",
        "term",
        "expiry",
        "expiration",
        "expires",
        "renew",
        "renewal",
        "notice",
        "termination",
        "payment",
        "payable",
        "invoice",
        "delivery",
        "deliver",
        "deadline",
        "within",
        "days",
        "weeks",
        "months",
        "years",
        "milestone",
        "report",
        "obligation",
        "shall",
        "must",
        "required",
        "due",
        "confidential",
        "indemnify",
        "indemnification",
        "intellectual property",
        "ownership",
        "license",
        "data",
        "security",
        "audit",
        "reimburse"
    )

    selected = []

    for line in lines:

        lower = line.lower()

        if any(
            keyword in lower
            for keyword in keywords
        ):
            selected.append(line)

    # Also include explicit dates.
    for line in lines:

        if re.search(
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            line
        ):

            selected.append(line)

        elif re.search(
            r"\b(?:jan(?:uary)?|feb(?:ruary)?|"
            r"mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
            r"jul(?:y)?|aug(?:ust)?|"
            r"sep(?:t(?:ember)?)?|oct(?:ober)?|"
            r"nov(?:ember)?|dec(?:ember)?)\b",
            line,
            flags=re.IGNORECASE
        ):

            selected.append(line)

    unique = list(
        dict.fromkeys(selected)
    )

    source = "\n".join(unique)

    if len(source) <= MAX_SOURCE_CHARS:
        return source

    return (
        source[:MAX_SOURCE_CHARS].rstrip()
        + "\n[Additional candidate lines omitted]"
    )


# =========================================================
# LOCAL FALLBACK EXTRACTION
# =========================================================

def _fallback_extract(
    source: str
) -> dict:

    lines = [
        line.strip()
        for line in source.splitlines()
        if line.strip()
    ]

    important_dates = []
    obligations = []
    renewal_alerts = []
    general_notes = []

    date_patterns = [

        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

        r"\b(?:jan(?:uary)?|feb(?:ruary)?|"
        r"mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
        r"jul(?:y)?|aug(?:ust)?|"
        r"sep(?:t(?:ember)?)?|oct(?:ober)?|"
        r"nov(?:ember)?|dec(?:ember)?)\s+"
        r"\d{1,2}(?:st|nd|rd|th)?"
        r"(?:,?\s+\d{4})?\b",
    ]

    for line in lines:

        lower = line.lower()

        # =================================================
        # IMPORTANT DATES
        # =================================================

        matched_date = any(
            re.search(
                pattern,
                line,
                flags=re.IGNORECASE
            )
            for pattern in date_patterns
        )

        if matched_date:

            if any(
                keyword in lower
                for keyword in (
                    "effective",
                    "commencement",
                    "start",
                    "execution",
                    "entered into"
                )
            ):
                label = "Effective / Start Date"

            elif any(
                keyword in lower
                for keyword in (
                    "expiry",
                    "expiration",
                    "expires",
                    "end date"
                )
            ):
                label = "Expiry / End Date"

            elif "renew" in lower:
                label = "Renewal Date"

            elif "terminat" in lower:
                label = "Termination Date"

            else:
                label = "Important Date"

            important_dates.append(
                {
                    "label": label,
                    "value": line,
                    "source": line[:350],
                    "notes": (
                        "Extracted from the contract text."
                    )
                }
            )

        # =================================================
        # OBLIGATION DETECTION
        # =================================================

        is_obligation = (
            any(
                keyword in lower
                for keyword in (
                    "shall",
                    "must",
                    "required to",
                    "is due",
                    "payable",
                    "notice period",
                    "renewal",
                    "deliver",
                    "provide",
                    "reimburse",
                    "indemnify",
                    "protect",
                    "maintain",
                    "notify"
                )
            )
            or re.search(
                r"\b(?:within|in)\s+\d+\s+"
                r"(?:day|days|week|weeks|month|months|year|years)\b",
                lower
            )
        )

        if is_obligation:

            kind = _detect_obligation_type(
                line
            )

            deadline = _detect_deadline(
                line
            )

            responsible_party = (
                _detect_responsible_party(
                    line
                )
            )

            obligations.append(
                {
                    "obligation_type": kind,

                    "requirement": line,

                    "deadline": deadline,

                    "responsible_party":
                        responsible_party,

                    "source": line[:350],

                    "notes": (
                        "Extracted from the contract text; "
                        "verify the full clause wording."
                    )
                }
            )

            if "renew" in lower:

                renewal_alerts.append(
                    line
                )

    # =====================================================
    # DEDUPLICATION
    # =====================================================

    def dedupe(items):

        seen = set()
        output = []

        for item in items:

            key = json.dumps(
                item,
                sort_keys=True,
                ensure_ascii=False
            )

            if key not in seen:

                seen.add(key)
                output.append(item)

        return output

    important_dates = dedupe(
        important_dates
    )[:MAX_DATES]

    obligations = dedupe(
        obligations
    )[:MAX_OBLIGATIONS]

    renewal_alerts = list(
        dict.fromkeys(
            renewal_alerts
        )
    )[:MAX_RENEWAL_ALERTS]

    if not important_dates and not obligations:

        general_notes.append(
            "No clear date or obligation statements "
            "were detected in the supplied contract text."
        )

    else:

        general_notes.append(
            "Some items were extracted locally. "
            "Review the source wording before using "
            "the result."
        )

    return {
        "important_dates":
            important_dates,

        "obligations":
            obligations,

        "renewal_alerts":
            renewal_alerts,

        "general_notes":
            general_notes
    }


# =========================================================
# NORMALIZE AI RESULT
# =========================================================

def _normalize_ai_result(
    parsed: dict
) -> dict:

    important_dates = (
        parsed.get(
            "important_dates",
            []
        )
        or []
    )

    obligations = (
        parsed.get(
            "obligations",
            []
        )
        or []
    )

    renewal_alerts = (
        parsed.get(
            "renewal_alerts",
            []
        )
        or []
    )

    general_notes = (
        parsed.get(
            "general_notes",
            []
        )
        or []
    )

    normalized_dates = []

    for item in important_dates:

        if not isinstance(
            item,
            dict
        ):
            continue

        normalized_dates.append(
            {
                "label":
                    str(
                        item.get(
                            "label",
                            "Important Date"
                        )
                    ),

                "value":
                    str(
                        item.get(
                            "value",
                            "Not specified"
                        )
                    ),

                "source":
                    str(
                        item.get(
                            "source",
                            ""
                        )
                    ),

                "notes":
                    str(
                        item.get(
                            "notes",
                            ""
                        )
                    )
            }
        )

    normalized_obligations = []

    for item in obligations:

        if not isinstance(
            item,
            dict
        ):
            continue

        requirement = str(
            item.get(
                "requirement",
                ""
            )
        ).strip()

        responsible_party = str(
            item.get(
                "responsible_party",
                "Not specified"
            )
        ).strip()

        # If AI failed to identify party,
        # use deterministic extraction.
        if (
            not responsible_party
            or responsible_party.lower()
            in (
                "not specified",
                "unknown",
                "n/a",
                "none"
            )
        ):

            responsible_party = (
                _detect_responsible_party(
                    requirement
                )
            )

        deadline = str(
            item.get(
                "deadline",
                "Not specified"
            )
        ).strip()

        if (
            not deadline
            or deadline.lower()
            in (
                "not specified",
                "unknown",
                "n/a",
                "none"
            )
        ):

            deadline = _detect_deadline(
                requirement
            )

        obligation_type = str(
            item.get(
                "obligation_type",
                "Other"
            )
        ).strip()

        if (
            not obligation_type
            or obligation_type.lower()
            == "other"
        ):

            obligation_type = (
                _detect_obligation_type(
                    requirement
                )
            )

        normalized_obligations.append(
            {
                "obligation_type":
                    obligation_type,

                "requirement":
                    requirement,

                "deadline":
                    deadline,

                "responsible_party":
                    responsible_party,

                "source":
                    str(
                        item.get(
                            "source",
                            requirement[:350]
                        )
                    ),

                "notes":
                    str(
                        item.get(
                            "notes",
                            "Review the original contract wording."
                        )
                    )
            }
        )

    # =====================================================
    # De-duplicate
    # =====================================================

    def dedupe(items):

        seen = set()
        result = []

        for item in items:

            key = json.dumps(
                item,
                sort_keys=True,
                ensure_ascii=False
            )

            if key not in seen:

                seen.add(key)
                result.append(item)

        return result

    normalized_dates = dedupe(
        normalized_dates
    )[:MAX_DATES]

    normalized_obligations = dedupe(
        normalized_obligations
    )[:MAX_OBLIGATIONS]

    renewal_alerts = list(
        dict.fromkeys(
            str(x)
            for x in renewal_alerts
        )
    )[:MAX_RENEWAL_ALERTS]

    general_notes = list(
        dict.fromkeys(
            str(x)
            for x in general_notes
        )
    )

    return {
        "important_dates":
            normalized_dates,

        "obligations":
            normalized_obligations,

        "renewal_alerts":
            renewal_alerts,

        "general_notes":
            general_notes
    }


# =========================================================
# API ENDPOINT
# =========================================================

@router.post(
    "/extract",
    response_model=ObligationsResponse
)
def extract_obligations(
    payload: ObligationRequest,
    current_user=Depends(get_current_user)
):

    # =====================================================
    # API KEY
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
    # BUILD SOURCE
    # =====================================================

    source = _candidate_lines(
        payload.contract_text
    )

    if not source:

        raise HTTPException(
            status_code=422,
            detail=(
                "No likely date or obligation clauses "
                "were found in the supplied contract text."
            )
        )

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = """
You are an expert contract information extraction assistant.

Extract ONLY information that is explicitly present
in the supplied contract text.

Your task is to identify:

1. Important dates
2. Deadlines
3. Renewal details
4. Concrete contractual obligations
5. Responsible parties

IMPORTANT RULES:

- Never invent information.
- Preserve dates and numbers exactly when possible.
- Identify the party responsible for each obligation.
- If the sentence begins with "Client shall", the responsible party is "Client".
- If the sentence begins with "Provider shall", the responsible party is "Provider".
- If it says "Each party shall", use "Both parties".
- If it says "Either party may", use "Either party".
- If the responsible party is explicitly named, always return it.
- Do not return "Not specified" when the responsible party can be determined from the wording.
- Keep each obligation as a complete meaningful sentence or clause.
- Do not split one obligation into unrelated fragments.
- Do not invent deadlines.
- If no deadline exists, use "Not specified".
- Do not provide legal advice.

Return ONLY valid JSON.

Use exactly this structure:

{
  "important_dates": [
    {
      "label": "Effective / Start Date",
      "value": "string",
      "source": "string",
      "notes": "string"
    }
  ],

  "obligations": [
    {
      "obligation_type": "Payment",
      "requirement": "string",
      "deadline": "string",
      "responsible_party": "Client",
      "source": "string",
      "notes": "string"
    }
  ],

  "renewal_alerts": [
    "string"
  ],

  "general_notes": [
    "string"
  ]
}

Allowed obligation types:

Payment
Delivery
Notice
Reporting
Renewal
Termination
Confidentiality
Indemnification
Intellectual Property
Data Protection
Audit
Other

Return no Markdown and no code fences.
""".strip()

    # =====================================================
    # USER PROMPT
    # =====================================================

    user_prompt = (
        "Extract important dates, deadlines, "
        "renewals, and concrete obligations "
        "from the following contract text.\n\n"
        "CONTRACT TEXT:\n\n"
        + source
    )

    # =====================================================
    # GROQ CLIENT
    # =====================================================

    client = Groq(
        api_key=api_key
    )

    try:

        completion = (
            client.chat.completions.create(
                model=GROQ_MODEL,

                temperature=0.1,

                max_tokens=2500,

                response_format={
                    "type": "json_object"
                },

                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
        )

        raw = (
            completion
            .choices[0]
            .message
            .content
            or ""
        ).strip()

        # =================================================
        # DEBUG OUTPUT
        # =================================================

        print(
            "\n========== DATES & OBLIGATIONS AI RESPONSE =========="
        )

        print(raw)

        print(
            "======================================================\n"
        )

        # =================================================
        # PARSE AI RESPONSE
        # =================================================

        try:

            parsed = _extract_json(
                raw
            )

            normalized = (
                _normalize_ai_result(
                    parsed
                )
            )

            return (
                ObligationsResponse.model_validate(
                    normalized
                )
            )

        except Exception as parse_error:

            print(
                "\n========== AI PARSE FAILED =========="
            )

            print(
                str(parse_error)
            )

            print(
                "Using local fallback extraction..."
            )

            print(
                "=====================================\n"
            )

            fallback = _fallback_extract(
                source
            )

            return (
                ObligationsResponse.model_validate(
                    fallback
                )
            )

    except Exception as exc:

        message = str(exc)

        lower_message = (
            message.lower()
        )

        print(
            "\n========== DATES & OBLIGATIONS ERROR =========="
        )

        print(message)

        print(
            "===============================================\n"
        )

        # =================================================
        # FALLBACK FOR AI LIMIT / JSON ERRORS
        # =================================================

        if (
            "request too large"
            in lower_message

            or "tokens per minute"
            in lower_message

            or "rate_limit_exceeded"
            in lower_message

            or "json"
            in lower_message

            or "schema"
            in lower_message

            or "validation"
            in lower_message
        ):

            fallback = _fallback_extract(
                source
            )

            return (
                ObligationsResponse.model_validate(
                    fallback
                )
            )

        # =================================================
        # GENERIC ERROR
        # =================================================

        raise HTTPException(
            status_code=500,
            detail=(
                "Date and obligation extraction failed: "
                f"{message}"
            )
        )