from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.connection import get_db
from models.user import User


# Load environment variables from .env
load_dotenv()


# JWT configuration
SECRET_KEY = os.getenv(
    "JWT_SECRET",
    "change-this-secret-key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Bearer token authentication
security = HTTPBearer()


# --------------------------------------------------
# PASSWORD FUNCTIONS
# --------------------------------------------------

def hash_password(password: str) -> str:
    """Hash a user's password."""
    
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """Verify a password against its hash."""
    
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# --------------------------------------------------
# JWT TOKEN
# --------------------------------------------------

def create_access_token(user_id: int) -> str:
    """Create a JWT access token for the user."""

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# --------------------------------------------------
# CURRENT USER
# --------------------------------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db)
):
    """
    Get the currently authenticated user
    from the JWT bearer token.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    # Get token from Authorization header
    token = credentials.credentials

    try:

        # Decode JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get user ID from token
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    # Find user in database
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise credentials_exception

    return user