from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from sqlalchemy.orm import Session

from database.connection import get_db
from models.user import User
from models.analysis import Analysis
from models.clause import Clause
from models.recommendation import Recommendation
from services.auth_service import get_current_user
from services.authorization_service import get_owned_contract


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)


REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# MARKDOWN REPORT
# ---------------------------------------------------------

@router.get("/{contract_id}/markdown")
def download_markdown_report(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contract = get_owned_contract(
        contract_id=contract_id,
        db=db,
        current_user=current_user,
    )

    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.contract_id == contract_id
        )
        .order_by(Analysis.id.desc())
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No analysis found.",
        )

    clauses = (
        db.query(Clause)
        .filter(
            Clause.analysis_id == analysis.id
        )
        .all()
    )

    recommendations = (
        db.query(Recommendation)
        .filter(
            Recommendation.analysis_id == analysis.id
        )
        .all()
    )

    lines = []

    lines.append("# AI Legal Contract Risk Analysis")
    lines.append("")
    lines.append(f"## Contract: {contract.title}")
    lines.append("")
    lines.append(
        f"**Contract ID:** {contract.id}"
    )
    lines.append("")
    lines.append(
        f"**Risk Score:** {analysis.overall_risk_score}/100"
    )
    lines.append("")
    lines.append(
        f"**Risk Level:** {analysis.overall_risk_level}"
    )
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(
        analysis.summary or "No summary available."
    )
    lines.append("")

    lines.append("## Flagged Clauses")
    lines.append("")

    if clauses:
        for index, clause in enumerate(clauses, start=1):
            lines.append(
                f"### Clause {index}: {clause.category}"
            )
            lines.append("")
            lines.append(
                f"**Severity:** {clause.severity}"
            )
            lines.append("")
            lines.append(
                f"**Original:** {clause.original_snippet}"
            )
            lines.append("")
            lines.append(
                f"**Issue:** {clause.issue_summary}"
            )
            lines.append("")
            lines.append(
                f"**Suggested Revision:** {clause.suggested_revision}"
            )
            lines.append("")
    else:
        lines.append("No flagged clauses found.")
        lines.append("")

    lines.append("## Recommendations")
    lines.append("")

    if recommendations:
        for index, item in enumerate(
            recommendations,
            start=1
        ):
            lines.append(
                f"{index}. **{item.title}**"
            )
            lines.append(
                f"   {item.description}"
            )
            lines.append(
                f"   Importance: {item.importance}"
            )
            lines.append("")
    else:
        lines.append("No recommendations found.")
        lines.append("")

    content = "\n".join(lines)

    report_path = REPORTS_DIR / (
        f"contract_{contract_id}_report.md"
    )

    report_path.write_text(
        content,
        encoding="utf-8",
    )

    return FileResponse(
        path=str(report_path),
        media_type="text/markdown",
        filename=report_path.name,
    )


# ---------------------------------------------------------
# PDF REPORT
# ---------------------------------------------------------

@router.get("/{contract_id}/pdf")
def download_pdf_report(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contract = get_owned_contract(
        contract_id=contract_id,
        db=db,
        current_user=current_user,
    )

    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.contract_id == contract_id
        )
        .order_by(Analysis.id.desc())
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No analysis found.",
        )

    clauses = (
        db.query(Clause)
        .filter(
            Clause.analysis_id == analysis.id
        )
        .all()
    )

    recommendations = (
        db.query(Recommendation)
        .filter(
            Recommendation.analysis_id == analysis.id
        )
        .all()
    )

    pdf_path = REPORTS_DIR / (
        f"contract_{contract_id}_report.pdf"
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=15,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=8,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
    )

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
    )

    story = []

    # Title
    story.append(
        Paragraph(
            "AI Legal Contract Risk Analysis",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"Contract: {contract.title}",
            body_style,
        )
    )

    story.append(
        Paragraph(
            f"Contract ID: {contract.id}",
            body_style,
        )
    )

    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            small_style,
        )
    )

    story.append(Spacer(1, 15))

    # Risk summary table
    risk_data = [
        [
            Paragraph("<b>Risk Score</b>", body_style),
            Paragraph("<b>Risk Level</b>", body_style),
        ],
        [
            f"{analysis.overall_risk_score}/100",
            analysis.overall_risk_level,
        ],
    ]

    risk_table = Table(
        risk_data,
        colWidths=[2.5 * inch, 2.5 * inch],
    )

    risk_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
            ]
        )
    )

    story.append(risk_table)
    story.append(Spacer(1, 15))

    # Summary
    story.append(
        Paragraph(
            "Summary",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            analysis.summary or "No summary available.",
            body_style,
        )
    )

    # Flagged clauses
    story.append(
        Paragraph(
            "Flagged Clauses",
            heading_style,
        )
    )

    if clauses:
        for index, clause in enumerate(
            clauses,
            start=1
        ):
            story.append(
                Paragraph(
                    f"<b>Clause {index}: "
                    f"{clause.category}</b>",
                    body_style,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Severity:</b> "
                    f"{clause.severity}",
                    body_style,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Original Clause:</b> "
                    f"{clause.original_snippet}",
                    body_style,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Issue:</b> "
                    f"{clause.issue_summary}",
                    body_style,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Suggested Revision:</b> "
                    f"{clause.suggested_revision}",
                    body_style,
                )
            )

            story.append(Spacer(1, 8))
    else:
        story.append(
            Paragraph(
                "No flagged clauses found.",
                body_style,
            )
        )

    # Recommendations
    story.append(
        Paragraph(
            "Recommendations",
            heading_style,
        )
    )

    if recommendations:
        for index, item in enumerate(
            recommendations,
            start=1
        ):
            story.append(
                Paragraph(
                    f"<b>{index}. {item.title}</b>",
                    body_style,
                )
            )

            story.append(
                Paragraph(
                    item.description,
                    body_style,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Importance:</b> "
                    f"{item.importance}",
                    small_style,
                )
            )

            story.append(Spacer(1, 6))
    else:
        story.append(
            Paragraph(
                "No recommendations found.",
                body_style,
            )
        )

    document.build(story)

    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=pdf_path.name,
    )