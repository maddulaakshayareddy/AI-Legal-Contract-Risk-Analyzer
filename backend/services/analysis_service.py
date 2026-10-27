
import json

from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.clause import Clause
from models.contract import Contract
from models.recommendation import Recommendation

from services.gemini_service import analyze_contract
from services.document_parser import verify_clause_evidence


def _as_text(value, default=""):
    """Convert a value into safe display text."""
    if value is None:
        return default

    if isinstance(value, str):
        return value

    return str(value)


def _as_list(value):
    """Return a list or an empty list for unexpected AI output."""
    return value if isinstance(value, list) else []


def _recommendation_title(item):
    """Extract a recommendation title from a string or dictionary."""
    if isinstance(item, dict):
        return (
            item.get("title")
            or item.get("recommendation")
            or item.get("suggestion")
            or "Recommendation"
        )

    return _as_text(item, "Recommendation")


def _recommendation_description(item):
    """Extract a recommendation description."""
    if isinstance(item, dict):
        description = (
            item.get("description")
            or item.get("reason")
            or item.get("explanation")
            or item.get("recommendation")
            or item.get("suggestion")
        )

        if description:
            return _as_text(description)

        return json.dumps(item, ensure_ascii=False)

    return _as_text(item)


def _protection_title(item):
    """Extract the title of a missing standard protection."""
    if isinstance(item, dict):
        return (
            item.get("protection")
            or item.get("title")
            or item.get("name")
            or "Missing Protection"
        )

    return _as_text(item, "Missing Protection")


def run_contract_analysis(
    contract: Contract,
    db: Session,
):
    """
    Analyze a contract, verify flagged clause evidence,
    and save analysis results to PostgreSQL.
    """

    if not contract.raw_text or not contract.raw_text.strip():
        raise ValueError(
            "The contract does not contain readable text."
        )

    # 1. Analyze the contract using the existing Groq integration.
    result = analyze_contract(contract.raw_text)

    if not isinstance(result, dict):
        raise ValueError(
            "The AI analysis returned an invalid result."
        )

    # 2. Verify flagged clause quotations.
    flagged_clauses = _as_list(
        result.get("flagged_clauses")
    )

    verified_flagged_clauses = []

    for item in flagged_clauses:
        if not isinstance(item, dict):
            continue

        original_snippet = _as_text(
            item.get("original_snippet")
            or item.get("snippet")
        )

        # Keep the analysis running even if evidence lookup fails.
        try:
            evidence = verify_clause_evidence(
                original_snippet=original_snippet,
                contract_text=contract.raw_text,
                file_path=contract.file_path,
                file_type=contract.file_type,
            )

            if not isinstance(evidence, dict):
                raise ValueError(
                    "Evidence verification returned an invalid result."
                )

            enriched_item = {
                **item,
                "original_snippet": original_snippet,
                "evidence_verified": bool(
                    evidence.get("evidence_verified", False)
                ),
                "page_number": evidence.get("page_number"),
                "evidence_status": evidence.get(
                    "evidence_status",
                    "page_lookup_failed",
                ),
            }

        except Exception:
            enriched_item = {
                **item,
                "original_snippet": original_snippet,
                "evidence_verified": False,
                "page_number": None,
                "evidence_status": "page_lookup_failed",
            }

        verified_flagged_clauses.append(enriched_item)

    # Add evidence metadata to the immediate analysis result.
    result["flagged_clauses"] = verified_flagged_clauses

    try:
        # 3. Create the main analysis record.
        analysis = Analysis(
            contract_id=contract.id,
            overall_risk_score=result.get(
                "overall_risk_score",
                0,
            ),
            overall_risk_level=_as_text(
                result.get("overall_risk_level"),
                "Unknown",
            ),
            summary=_as_text(result.get("summary")),
            categories_json=json.dumps(
                result.get("category_risks", []),
                ensure_ascii=False,
            ),
        )

        db.add(analysis)
        db.flush()

        # 4. Save flagged clauses using existing model fields.
        for item in verified_flagged_clauses:
            clause = Clause(
                contract_id=contract.id,
                analysis_id=analysis.id,
                category=_as_text(
                    item.get("category"),
                    "General",
                ),
                original_snippet=_as_text(
                    item.get("original_snippet")
                ),
                issue_summary=_as_text(
                    item.get("issue_summary")
                    or item.get("issue")
                ),
                severity=_as_text(
                    item.get("severity"),
                    "Medium",
                ),
                suggested_revision=_as_text(
                    item.get("suggested_revision")
                ),
            )

            db.add(clause)

        # 5. Save general recommendations.
        for item in _as_list(result.get("recommendations")):
            if isinstance(item, dict):
                importance = _as_text(
                    item.get("importance"),
                    "Medium",
                )
            else:
                importance = "Medium"

            recommendation = Recommendation(
                contract_id=contract.id,
                analysis_id=analysis.id,
                type="recommendation",
                title=_recommendation_title(item),
                description=_recommendation_description(item),
                importance=importance,
            )

            db.add(recommendation)

        # 6. Save missing standard protections.
        for item in _as_list(
            result.get("missing_standard_protections")
        ):
            if isinstance(item, dict):
                importance = _as_text(
                    item.get("importance"),
                    "Medium",
                )
                description = (
                    item.get("reason")
                    or item.get("description")
                    or item.get("explanation")
                )

                if not description:
                    description = _recommendation_description(item)
                else:
                    description = _as_text(description)

            else:
                importance = "Medium"
                description = _recommendation_description(item)

            recommendation = Recommendation(
                contract_id=contract.id,
                analysis_id=analysis.id,
                type="missing_protection",
                title=_protection_title(item),
                description=description,
                importance=importance,
            )

            db.add(recommendation)

        # 7. Save all related records in one transaction.
        db.commit()
        db.refresh(analysis)

        return {
            "analysis": analysis,
            "result": result,
        }

    except Exception:
        db.rollback()
        raise
