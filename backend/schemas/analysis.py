from typing import List, Optional

from pydantic import BaseModel, Field


class RiskClause(BaseModel):
    category: str
    original_snippet: str
    issue_summary: str
    severity: str
    suggested_revision: Optional[str] = None


class MissingProtection(BaseModel):
    protection: str
    explanation: str
    importance: str


class CategoryRisk(BaseModel):
    category: str
    score: int = Field(ge=1, le=100)
    risk_level: str
    summary: str


class AnalysisResult(BaseModel):
    overall_risk_score: int = Field(
        ge=1,
        le=100
    )
    overall_risk_level: str
    summary: str
    category_risks: List[CategoryRisk]
    flagged_clauses: List[RiskClause]
    missing_standard_protections: List[MissingProtection]
    recommendations: List[str]


class AnalysisOut(BaseModel):
    id: int
    contract_id: int
    overall_risk_score: int
    overall_risk_level: str
    summary: Optional[str] = None

    class Config:
        from_attributes = True