import os

from fastapi import APIRouter, HTTPException
from groq import Groq
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/api/clause-comparison",
    tags=["Clause Comparison"],
)


class ClauseComparisonRequest(BaseModel):
    clause_a: str = Field(
        min_length=10,
        max_length=10000
    )

    clause_b: str = Field(
        min_length=10,
        max_length=10000
    )


@router.post("/compare")
def compare_clauses(
    payload: ClauseComparisonRequest
):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Groq API configuration is missing."
        )

    prompt = f"""
You are a legal document comparison assistant.

Compare the following two contract clauses.

CLAUSE A:
{payload.clause_a}

CLAUSE B:
{payload.clause_b}

Provide the comparison using exactly these sections:

1. Overall Difference
Explain the main difference between the two clauses in simple language.

2. Key Changes
List the important wording, obligation, right, duration, payment, termination,
confidentiality, liability, or other changes that appear between the clauses.

3. Practical Impact
Explain what each major change could mean for the parties.

4. Points to Review
Identify wording that deserves closer review.

5. Plain-English Summary
Give a short final explanation that a non-legal user can understand.

Important:
- Compare only the text provided.
- Do not invent information that is not present.
- Clearly state when the clauses are substantially similar.
- Do not present the output as legal advice.
"""

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        result = response.choices[0].message.content

        if not result:
            raise HTTPException(
                status_code=500,
                detail="No comparison result was generated."
            )

        return {
            "comparison": result
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Clause comparison failed: {str(exc)}"
        ) from exc