python
import json
import os
import re

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from database.connection import Base, engine, SessionLocal

from api.routes.auth import router as auth_router
from api.routes.contracts import router as contracts_router
from api.routes.analysis import router as analysis_router
from api.routes.qa import router as qa_router
from api.routes.reports import router as reports_router
from api.routes.scan import router as scan_router
from api.routes.password_reset import router as password_reset_router
from api.routes.document_generator import router as document_generator_router
from api.routes.clause_comparison import router as clause_comparison_router
from api.routes.language import router as language_router
from api.routes.version_diff import router as version_diff_router
from api.routes.obligations import router as obligations_router
from api.routes.evidence_sources import router as evidence_sources_router
from api.routes.audit import router as audit_router

from models.audit_log import AuditLog
from models.user import User
from models.contract import Contract
from models.analysis import Analysis
from models.clause import Clause
from models.recommendation import Recommendation
from models.qa import Question


load_dotenv()


app = FastAPI(
    title="AI Legal Contract Risk Analyzer",
    description="AI-powered contract risk analysis system",
    version="1.0.0",
)


# Create database tables after importing the models.
# This preserves the existing database initialization behavior.
Base.metadata.create_all(bind=engine)


# Configure frontend access.
# Add your deployed frontend origin through the CORS_ORIGINS
# environment variable in Render.
default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

configured_origins = os.getenv("CORS_ORIGINS", "").strip()

if configured_origins:
    allowed_origins = [
        origin.strip().rstrip("/")
        for origin in configured_origins.split(",")
        if origin.strip()
    ]
else:
    allowed_origins = default_origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Record meaningful user actions without logging routine GET requests.
def resolve_audit_action(method: str, path: str):
    rules = [
        (
            "POST",
            re.compile(r"^/api/contracts/?$"),
            "Contract uploaded",
        ),
        (
            "POST",
            re.compile(r"^/api/contracts/text$"),
            "Contract created from text",
        ),
        (
            "POST",
            re.compile(r"^/api/analysis/\d+$"),
            "Contract analysis requested",
        ),
        (
            "POST",
            re.compile(r"^/api/qa/?$"),
            "Contract question asked",
        ),
        (
            "GET",
            re.compile(r"^/api/reports/\d+/(?:pdf|md)$"),
            "Report downloaded",
        ),
        (
            "POST",
            re.compile(r"^/api/scan/upload$"),
            "Scanned contract uploaded",
        ),
        (
            "POST",
            re.compile(r"^/api/document-generator/generate$"),
            "Document generated",
        ),
        (
            "POST",
            re.compile(r"^/api/document-generator/generate-pdf$"),
            "Generated document downloaded",
        ),
        (
            "POST",
            re.compile(r"^/api/clause-comparison/compare$"),
            "Clause comparison performed",
        ),
        (
            "POST",
            re.compile(r"^/api/version-diff/compare$"),
            "Contract version comparison performed",
        ),
        (
            "POST",
            re.compile(r"^/api/obligations/extract$"),
            "Dates and obligations extracted",
        ),
        (
            "POST",
            re.compile(r"^/api/language/translate$"),
            "Contract text translated",
        ),
        (
            "POST",
            re.compile(r"^/api/language/translate-file$"),
            "Document translated",
        ),
        (
            "POST",
            re.compile(r"^/api/language/download-pdf$"),
            "Translated PDF downloaded",
        ),
        (
            "POST",
            re.compile(r"^/api/language/download-docx$"),
            "Translated Word document downloaded",
        ),
        (
            "POST",
            re.compile(r"^/api/password/change$"),
            "Password changed",
        ),
        (
            "POST",
            re.compile(r"^/api/password/generate-code$"),
            "Recovery code generated",
        ),
    ]

    for rule_method, pattern, action in rules:
        if method == rule_method and pattern.fullmatch(path):
            return action

    return None


def extract_contract_id(path: str):
    patterns = [
        r"^/api/contracts/(\d+)$",
        r"^/api/analysis/(\d+)$",
        r"^/api/reports/(\d+)/(?:pdf|md)$",
        r"^/api/evidence/contract/(\d+)$",
    ]

    for pattern in patterns:
        match = re.fullmatch(pattern, path)

        if match:
            return int(match.group(1))

    return None


@app.middleware("http")
async def audit_request_middleware(
    request: Request,
    call_next,
):
    # Let FastAPI process the request first.
    response = await call_next(request)

    path = request.url.path
    method = request.method.upper()

    action = resolve_audit_action(method, path)

    if not action or path.startswith("/api/audit"):
        return response

    # Identify the authenticated user from the JWT.
    actor_subject = None
    auth_header = request.headers.get("authorization", "")

    if auth_header.lower().startswith("bearer "):
        token_value = auth_header.split(" ", 1)[1].strip()

        try:
            from jose import jwt

            secret = os.getenv("JWT_SECRET")

            if secret:
                payload = jwt.decode(
                    token_value,
                    secret,
                    algorithms=["HS256"],
                )

                actor_subject = payload.get("sub")

        except Exception:
            # Audit logging must not break the original request.
            actor_subject = None

    # Do not create audit entries for anonymous requests.
    if actor_subject is None:
        return response

    contract_id = extract_contract_id(path)

    metadata = {
        "query": request.url.query or None,
        "status_code": response.status_code,
    }

    db = None

    try:
        db = SessionLocal()

        audit_entry = AuditLog(
            actor_subject=str(actor_subject),
            action=action,
            method=method[:20],
            path=path[:500],
            status_code=response.status_code,
            contract_id=contract_id,
            metadata_json=json.dumps(metadata),
        )

        db.add(audit_entry)
        db.commit()

    except Exception:
        # Audit failures must never prevent users from using the API.
        if db is not None:
            try:
                db.rollback()
            except Exception:
                pass

    finally:
        if db is not None:
            try:
                db.close()
            except Exception:
                pass

    return response


# Register all existing API routers.
app.include_router(auth_router)
app.include_router(contracts_router)
app.include_router(analysis_router)
app.include_router(qa_router)
app.include_router(reports_router)
app.include_router(scan_router)
app.include_router(password_reset_router)
app.include_router(document_generator_router)
app.include_router(clause_comparison_router)
app.include_router(language_router)
app.include_router(version_diff_router)
app.include_router(obligations_router)
app.include_router(evidence_sources_router)
app.include_router(audit_router)


@app.get("/")
def root():
    return {
        "message": "AI Legal Contract Risk Analyzer API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
