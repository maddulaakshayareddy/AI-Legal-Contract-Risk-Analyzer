import re
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.connection import get_db
from services.auth_service import get_current_user
from services.authorization_service import get_owned_contract


router = APIRouter(
    prefix="/api/evidence",
    tags=["Evidence Sources"]
)


def _find_clause_in_text(
    raw_text: str,
    snippet: str
) -> Optional[dict]:
    if not raw_text or not snippet:
        return None

    # First try an exact case-insensitive match.
    match = re.search(
        re.escape(snippet.strip()),
        raw_text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # If whitespace differs between stored clause text
    # and contract text, allow arbitrary whitespace.
    if not match:
        words = re.findall(r"\S+", snippet.strip())

        if words:
            pattern = r"\s+".join(
                re.escape(word)
                for word in words
            )

            match = re.search(
                pattern,
                raw_text,
                flags=re.IGNORECASE | re.DOTALL
            )

    # Lightweight fallback:
    # look for a distinctive phrase.
    if not match:
        words = re.findall(
            r"[A-Za-z0-9]{5,}",
            snippet.lower()
        )

        for start in range(
            max(0, len(words) - 8),
            -1,
            -1
        ):
            phrase_words = words[start:start + 8]

            if len(phrase_words) < 3:
                continue

            pattern = r"\s+".join(
                re.escape(word)
                for word in phrase_words
            )

            match = re.search(
                pattern,
                raw_text,
                flags=re.IGNORECASE | re.DOTALL
            )

            if match:
                break

    if not match:
        return None

    start = match.start()
    end = match.end()

    line_number = (
        raw_text.count("\n", 0, start) + 1
    )

    lines_before = raw_text[:start].splitlines()

    section = None

    for line in reversed(lines_before[-40:]):
        candidate = line.strip()

        if not candidate:
            continue

        if re.match(
            r"^(?:section\s+)?\d+(?:\.\d+)*[.)]?\s+",
            candidate,
            re.IGNORECASE
        ):
            section = candidate[:180]
            break

        if (
            len(candidate) <= 100
            and candidate.upper() == candidate
            and any(ch.isalpha() for ch in candidate)
        ):
            section = candidate
            break

    context_start = max(
        0,
        start - 280
    )

    context_end = min(
        len(raw_text),
        end + 420
    )

    return {
        "matched": True,
        "line_number": line_number,
        "section": section,
        "start_char": start,
        "end_char": end,
        "context": raw_text[
            context_start:context_end
        ].strip(),
    }


@router.get("/contract/{contract_id}")
def get_contract_evidence(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Centralized ownership check.
    # Another user's contract is returned as 404.
    contract = get_owned_contract(
        contract_id=contract_id,
        db=db,
        current_user=current_user,
    )

    latest_analysis = db.execute(
        text(
            """
            SELECT id, created_at
            FROM analyses
            WHERE contract_id = :contract_id
            ORDER BY created_at DESC, id DESC
            LIMIT 1
            """
        ),
        {
            "contract_id": contract_id
        },
    ).mappings().first()

    if not latest_analysis:
        return {
            "contract_id": contract_id,
            "contract_title": contract.title,
            "analysis_id": None,
            "sources": [],
            "message": "No completed analysis found for this contract.",
        }

    clauses = db.execute(
        text(
            """
            SELECT
                id,
                category,
                original_snippet,
                issue_summary,
                severity,
                suggested_revision
            FROM clauses
            WHERE
                contract_id = :contract_id
                AND analysis_id = :analysis_id
            ORDER BY id ASC
            """
        ),
        {
            "contract_id": contract_id,
            "analysis_id": latest_analysis["id"],
        },
    ).mappings().all()

    sources = []

    raw_text = contract.raw_text or ""

    for clause in clauses:
        source = _find_clause_in_text(
            raw_text,
            clause["original_snippet"] or ""
        )

        sources.append(
            {
                "clause_id": clause["id"],
                "category": clause["category"],
                "severity": clause["severity"],
                "original_snippet": clause["original_snippet"],
                "issue_summary": clause["issue_summary"],
                "suggested_revision": clause["suggested_revision"],
                "source": source
                or {
                    "matched": False,
                    "line_number": None,
                    "section": None,
                    "start_char": None,
                    "end_char": None,
                    "context": None,
                },
            }
        )

    return {
        "contract_id": contract_id,
        "contract_title": contract.title,
        "file_name": contract.file_name,
        "file_type": contract.file_type,
        "analysis_id": latest_analysis["id"],
        "analysis_created_at": latest_analysis["created_at"],
        "sources": sources,
    }