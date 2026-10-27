from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from database.connection import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    file_name = Column(
        String(255),
        nullable=True
    )

    file_type = Column(
        String(50),
        nullable=True
    )

    file_path = Column(
        String(500),
        nullable=True
    )

    raw_text = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )