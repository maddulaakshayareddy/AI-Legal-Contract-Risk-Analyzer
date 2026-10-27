import json
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.connection import get_db
from models.audit_log import AuditLog
from services.auth_service import get_current_user
from services.authorization_service import get_owned_contract


router = APIRouter(
    prefix="/api/audit",
    tags=["Audit"]
)


ALLOWED_ACTIONS = {
    "Contract viewed": "ui://contract-view",
    "Source evidence viewed": "ui://source-evidence-view",
}


class AuditEventRequest(BaseModel):
    action: str = Field(
        min_length=1,
        max_length=100
    )
    contract_id: Optional[int] = None


@router.post("/event")
def create_audit_event(
    payload: AuditEventRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    path = ALLOWED_ACTIONS.get(payload.action)

    if not path:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audit action."
        )

    # If an audit event refers to a contract,
    # verify that the contract belongs to the logged-in user.
    if payload.contract_id is not None:
        get_owned_contract(
            contract_id=payload.contract_id,
            db=db,
            current_user=current_user,
        )

    actor_subject = str(current_user.id)

    # Avoid duplicate records caused by accidental
    # double-clicks or repeated UI event firing.
    cutoff = (
        datetime.now(timezone.utc)
        - timedelta(seconds=5)
    )

    recent = (
        db.query(AuditLog)
        .filter(
            AuditLog.actor_subject == actor_subject,
            AuditLog.action == payload.action,
            AuditLog.contract_id == payload.contract_id,
            AuditLog.created_at >= cutoff,
        )
        .order_by(
            AuditLog.created_at.desc()
        )
        .first()
    )

    if recent:
        return {
            "message": "Duplicate activity ignored",
            "id": recent.id,
            "duplicate": True,
        }

    row = AuditLog(
        actor_subject=actor_subject,
        action=payload.action,
        method="UI",
        path=path,
        status_code=200,
        contract_id=payload.contract_id,
        metadata_json=json.dumps(
            {
                "source": "explicit_user_action"
            }
        ),
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "message": "Audit event recorded",
        "id": row.id,
        "duplicate": False,
    }


@router.get("/logs")
def get_audit_logs(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    limit = max(
        1,
        min(limit, 200)
    )

    actor_subject = str(current_user.id)

    rows = (
        db.query(AuditLog)
        .filter(
            AuditLog.actor_subject == actor_subject
        )
        .order_by(
            AuditLog.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return {
        "logs": [
            {
                "id": row.id,
                "action": row.action,
                "method": row.method,
                "path": row.path,
                "status_code": row.status_code,
                "contract_id": row.contract_id,
                "metadata": (
                    json.loads(row.metadata_json)
                    if row.metadata_json
                    else None
                ),
                "created_at": row.created_at,
            }
            for row in rows
        ]
    }
