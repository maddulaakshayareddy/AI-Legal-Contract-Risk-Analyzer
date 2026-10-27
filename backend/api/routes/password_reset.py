import re
import secrets
import string

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database.connection import get_db
from models.user import User
from services.auth_service import get_current_user


router = APIRouter(
    prefix="/api/password",
    tags=["Password Recovery"],
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    recovery_code: str = Field(min_length=8, max_length=32)
    new_password: str = Field(min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


def validate_password(password: str) -> str | None:
    if len(password) < 8:
        return "Password must contain at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return "Password must contain at least one number."

    if not re.search(r"[^A-Za-z0-9]", password):
        return "Password must contain at least one special character."

    return None


def generate_recovery_code() -> str:
    alphabet = string.ascii_uppercase + string.digits

    return "-".join(
        "".join(
            secrets.choice(alphabet)
            for _ in range(4)
        )
        for _ in range(3)
    )


@router.post("/generate-code")
def generate_code(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recovery_code = generate_recovery_code()

    current_user.recovery_code_hash = pwd_context.hash(
        recovery_code
    )

    db.commit()

    return {
        "message": "Recovery code generated successfully.",
        "recovery_code": recovery_code,
    }


@router.post("/reset")
def reset_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    password_error = validate_password(
        payload.new_password
    )

    if password_error:
        raise HTTPException(
            status_code=400,
            detail=password_error,
        )

    user = (
        db.query(User)
        .filter(User.email == payload.email.lower())
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No account found with this email address.",
        )

    if not user.recovery_code_hash:
        raise HTTPException(
            status_code=400,
            detail=(
                "No recovery code is configured for this account. "
                "Log in and generate a recovery code from "
                "Settings → Login & Security."
            ),
        )

    if not pwd_context.verify(
        payload.recovery_code,
        user.recovery_code_hash,
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid recovery code.",
        )

    user.hashed_password = pwd_context.hash(
        payload.new_password
    )

    user.recovery_code_hash = None

    db.commit()

    return {
        "message": (
            "Password reset successfully. "
            "You can now log in with your new password."
        )
    }


@router.post("/change")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    password_error = validate_password(
        payload.new_password
    )

    if password_error:
        raise HTTPException(
            status_code=400,
            detail=password_error,
        )

    if not pwd_context.verify(
        payload.current_password,
        current_user.hashed_password,
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect.",
        )

    current_user.hashed_password = pwd_context.hash(
        payload.new_password
    )

    db.commit()

    return {
        "message": "Password changed successfully."
    }