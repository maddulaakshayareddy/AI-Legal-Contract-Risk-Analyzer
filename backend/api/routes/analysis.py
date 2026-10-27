
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from models.analysis import Analysis
from models.clause import Clause
from models.contract import Contract
from models.recommendation import Recommendation
from models.user import User

from services.analysis_service import run_contract_analysis
from services.auth_service import get_current_user
from services.authorization_service import get_owned_contract
from services.document_parser import verify_clause_evidence


router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"]
)


# ---------------------------------------------------------
# RUN NEW ANALYSIS
# ---------------------------------------------------------
@router.post("/{contract_id}")
def analyze_contract_endpoint(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contract = get_owned_contract(
        contract_id=contract_id,
        db=db,
        current_user=current_user
    )

    try:
        analysis_data = run_contract_analysis(
            contract,
            db
        )

        analysis = analysis_data["analysis"]
        result = analysis_data["result"]

        return {
            "id": analysis.id,
            "contract_id": contract.id,
            "overall_risk_score": result.get(
                "overall_risk_score",
                1
            ),
            "overall_risk_level": result.get(
                "overall_risk_level",
                "Low"
            ),
            "summary": result.get(
                "summary",
                ""
            ),
            "category_risks": result.get(
                "category_risks",
                []
            ),
            "flagged_clauses": result.get(
                "flagged_clauses",
                []
            ),
            "missing_standard_protections": result.get(
                "missing_standard_protections",
                []
            ),
            "recommendations": result.get(
                "recommendations",
                []
            ),
            "created_at": analysis.created_at
        }

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail=f"Contract analysis failed: {str(exc)}"
        ) from exc


# ---------------------------------------------------------
# ANALYSIS HISTORY
# ONE LATEST RECORD PER CONTRACT
# ---------------------------------------------------------
@router.get("/history")
def get_analysis_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analyses = (
        db.query(Analysis)
        .join(
            Contract,
            Analysis.contract_id == Contract.id
        )
        .filter(
            Contract.user_id == current_user.id
        )
        .order_by(
            Analysis.created_at.desc(),
            Analysis.id.desc()
        )
        .all()
    )

    history = []
    seen_contracts = set()

    # Keep only the latest analysis for each contract
    for analysis in analyses:

        if analysis.contract_id in seen_contracts:
            continue

        seen_contracts.add(
            analysis.contract_id
        )

        contract = (
            db.query(Contract)
            .filter(
                Contract.id == analysis.contract_id,
                Contract.user_id == current_user.id
            )
            .first()
        )

        history.append(
            {
                "id": analysis.id,
                "contract_id": analysis.contract_id,
                "contract_title": (
                    contract.title
                    if contract
                    else f"Contract {analysis.contract_id}"
                ),
                "overall_risk_score": (
                    analysis.overall_risk_score
                ),
                "overall_risk_level": (
                    analysis.overall_risk_level
                ),
                "summary": analysis.summary,
                "created_at": analysis.created_at
            }
        )

    return {
        "total": len(history),
        "history": history
    }


# ---------------------------------------------------------
# GET LATEST ANALYSIS FOR ONE CONTRACT
# ---------------------------------------------------------
@router.get("/contract/{contract_id}")
def get_contract_analysis(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contract = get_owned_contract(
        contract_id=contract_id,
        db=db,
        current_user=current_user
    )

    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.contract_id == contract.id
        )
        .order_by(
            Analysis.id.desc()
        )
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No analysis found."
        )

    # -----------------------------------------------------
    # CATEGORY RISKS
    # -----------------------------------------------------
    category_risks = []

    if analysis.categories_json:
        try:
            category_risks = json.loads(
                analysis.categories_json
            )

            if not isinstance(
                category_risks,
                list
            ):
                category_risks = []

        except (
            json.JSONDecodeError,
            TypeError
        ):
            category_risks = []

    # -----------------------------------------------------
    # FLAGGED CLAUSES + EVIDENCE VERIFICATION
    # -----------------------------------------------------
    clauses = (
        db.query(Clause)
        .filter(
            Clause.analysis_id == analysis.id
        )
        .all()
    )

    flagged_clauses = []

    for clause in clauses:

        evidence = verify_clause_evidence(
            original_snippet=clause.original_snippet or "",
            contract_text=contract.raw_text or "",
            file_path=contract.file_path,
            file_type=contract.file_type,
        )

        flagged_clauses.append(
            {
                "id": clause.id,
                "category": clause.category,
                "original_snippet": (
                    clause.original_snippet
                ),
                "issue_summary": (
                    clause.issue_summary
                ),
                "severity": clause.severity,
                "suggested_revision": (
                    clause.suggested_revision
                ),
                "evidence_verified": (
                    evidence["evidence_verified"]
                ),
                "page_number": (
                    evidence["page_number"]
                ),
                "evidence_status": (
                    evidence["evidence_status"]
                )
            }
        )

    # -----------------------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------------------
    recommendations = (
        db.query(Recommendation)
        .filter(
            Recommendation.analysis_id == analysis.id
        )
        .all()
    )

    normal_recommendations = []
    missing_protections = []

    for item in recommendations:

        item_data = {
            "id": item.id,
            "type": item.type,
            "title": item.title,
            "description": item.description,
            "importance": item.importance
        }

        if item.type == "missing_protection":
            missing_protections.append(
                item_data
            )
        else:
            normal_recommendations.append(
                item_data
            )

    # -----------------------------------------------------
    # RETURN COMPLETE ANALYSIS
    # -----------------------------------------------------
    return {
        "id": analysis.id,
        "contract_id": contract.id,
        "overall_risk_score": (
            analysis.overall_risk_score
        ),
        "overall_risk_level": (
            analysis.overall_risk_level
        ),
        "summary": analysis.summary,
        "category_risks": category_risks,
        "flagged_clauses": flagged_clauses,
        "missing_standard_protections": (
            missing_protections
        ),
        "recommendations": (
            normal_recommendations
        ),
        "created_at": analysis.created_at
    }
