import json

from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.clause import Clause
from models.contract import Contract
from models.recommendation import Recommendation

from services.gemini_service import analyze_contract


def run_contract_analysis(
    contract: Contract,
    db: Session
):
    """
    Analyze a contract with Gemini and save the complete
    analysis result into PostgreSQL.
    """

    if not contract.raw_text:
        raise ValueError("Contract does not contain any text.")

    # Ask Gemini to analyze the contract
    result = analyze_contract(contract.raw_text)

    # Create main analysis record
    analysis = Analysis(
        contract_id=contract.id,
        overall_risk_score=result.get(
            "overall_risk_score",
            1
        ),
        overall_risk_level=result.get(
            "overall_risk_level",
            "Low"
        ),
        summary=result.get(
            "summary",
            ""
        ),
        categories_json=json.dumps(
            result.get(
                "category_risks",
                []
            )
        ),
    )

    db.add(analysis)
    db.flush()

    # ---------------- FLAGGED CLAUSES ----------------

    flagged_clauses = result.get(
        "flagged_clauses",
        []
    )

    for item in flagged_clauses:
        clause = Clause(
            contract_id=contract.id,
            analysis_id=analysis.id,
            category=item.get(
                "category",
                "General"
            ),
            original_snippet=item.get(
                "original_snippet",
                item.get("snippet", "")
            ),
            issue_summary=item.get(
                "issue_summary",
                item.get("issue", "")
            ),
            severity=item.get(
                "severity",
                "Medium"
            ),
            suggested_revision=item.get(
                "suggested_revision",
                ""
            ),
        )

        db.add(clause)

    # ---------------- RECOMMENDATIONS ----------------

    recommendations = result.get(
        "recommendations",
        []
    )

    for item in recommendations:
        recommendation = Recommendation(
            contract_id=contract.id,
            analysis_id=analysis.id,
            type="recommendation",
            title=item.get(
                "title",
                "Recommendation"
            ),
            description=item.get(
                "description",
                ""
            ),
            importance=item.get(
                "importance",
                "Medium"
            ),
        )

        db.add(recommendation)

    # ---------------- MISSING PROTECTIONS ----------------

    missing_protections = result.get(
        "missing_standard_protections",
        []
    )

    for item in missing_protections:
        recommendation = Recommendation(
            contract_id=contract.id,
            analysis_id=analysis.id,
            type="missing_protection",
            title=item.get(
                "protection",
                item.get(
                    "title",
                    item.get(
                        "name",
                        "Missing Protection"
                    )
                )
            ),
            description=item.get(
                "reason",
                item.get(
                    "description",
                    item.get(
                        "explanation",
                        ""
                    )
                )
            ),
            importance=item.get(
                "importance",
                "Medium"
            ),
        )

        db.add(recommendation)

    # Save everything together
    db.commit()
    db.refresh(analysis)

    return {
        "analysis": analysis,
        "result": result,
    }