from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from database.connection import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    contract_id = Column(
        Integer,
        ForeignKey("contracts.id"),
        nullable=False,
        index=True
    )

    overall_risk_score = Column(
        Integer,
        nullable=False
    )

    overall_risk_level = Column(
        String(20),
        nullable=False
    )

    summary = Column(
        Text,
        nullable=True
    )

    categories_json = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )