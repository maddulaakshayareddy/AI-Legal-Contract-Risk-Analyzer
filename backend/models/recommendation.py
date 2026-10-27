from sqlalchemy import Column, Integer, String, Text, ForeignKey

from database.connection import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

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

    type = Column(
        String(50),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    importance = Column(
        String(20),
        nullable=False
    )