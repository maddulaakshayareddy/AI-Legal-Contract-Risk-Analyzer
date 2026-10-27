from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.contract import Contract


def get_owned_contract(
    contract_id: int,
    db: Session,
    current_user,
) -> Contract:
    """
    Return a contract only if it belongs to the logged-in user.

    A missing contract and another user's contract both return 404,
    so the API does not reveal whether another user's contract exists.
    """
    contract = (
        db.query(Contract)
        .filter(
            Contract.id == contract_id,
            Contract.user_id == current_user.id,
        )
        .first()
    )

    if contract is None:
        raise HTTPException(
            status_code=404,
            detail="Contract not found.",
        )

    return contract