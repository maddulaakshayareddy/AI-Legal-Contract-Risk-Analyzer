from database.connection import engine
from sqlalchemy import text

# Remove only the old/misleading view-evidence audit rows created while
# the audit system was being tested. Analysis and other meaningful events
# are preserved.
BAD_ACTIONS = ("Contract viewed", "Source evidence viewed")
BAD_PATHS = (
    "/api/audit/event",
    "/api/analysis/history",
)

with engine.begin() as conn:
    result = conn.execute(
        text(
            """
            DELETE FROM audit_logs
            WHERE action IN ('Contract viewed', 'Source evidence viewed')
              AND (
                    path IN ('/api/audit/event', '/api/analysis/history')
                    OR path LIKE '/api/contracts/%'
                    OR path LIKE '/api/evidence/contract/%'
                  )
            """
        )
    )

print(f"REMOVED {result.rowcount} OLD DUPLICATE VIEW/EVIDENCE AUDIT ROWS")
