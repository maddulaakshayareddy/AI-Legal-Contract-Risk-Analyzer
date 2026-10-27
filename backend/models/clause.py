from sqlalchemy import Column, Integer, String, Text, ForeignKey

from database.connection import Base


class Clause(Base):
    __tablename__ = "clauses"

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

    analysis_id = Column(
        Integer,
        ForeignKey("analyses.id"),
        nullable=False,
        index=True
    )

    category = Column(
        String(100),
        nullable=False
    )

    original_snippet = Column(
        Text,
        nullable=False
    )

    issue_summary = Column(
        Text,
        nullable=False
    )

    severity = Column(
        String(20),
        nullable=False
    )

    suggested_revision = Column(
        Text,
        nullable=True
    )