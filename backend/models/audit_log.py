from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database.connection import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_subject = Column(String(255), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    method = Column(String(20), nullable=False)
    path = Column(String(500), nullable=False)
    status_code = Column(Integer, nullable=False)
    contract_id = Column(Integer, nullable=True, index=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
