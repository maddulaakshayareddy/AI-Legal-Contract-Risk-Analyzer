import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured in backend/.env")

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-120b"


ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "overall_risk_score": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
        },
        "overall_risk_level": {
            "type": "string",
            "enum": ["Low", "Medium", "High"]
        },
        "summary": {
            "type": "string"
        },
        "category_risks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "risk_score": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "risk_level": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"]
                    },
                    "explanation": {"type": "string"}
                },
                "required": [
                    "category",
                    "risk_score",
                    "risk_level",
                    "explanation"
                ],
                "additionalProperties": False
            }
        },
        "flagged_clauses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "original_snippet": {"type": "string"},
                    "issue_summary": {"type": "string"},
                    "severity": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"]
                    },
                    "suggested_revision": {"type": "string"}
                },
                "required": [
                    "category",
                    "original_snippet",
                    "issue_summary",
                    "severity",
                    "suggested_revision"
                ],
                "additionalProperties": False
            }
        },
        "missing_standard_protections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "protection": {"type": "string"},
                    "reason": {"type": "string"},
                    "importance": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"]
                    }
                },
                "required": [
                    "protection",
                    "reason",
                    "importance"
                ],
                "additionalProperties": False
            }
        },
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "importance": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"]
                    }
                },
                "required": [
                    "title",
                    "description",
                    "importance"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": [
        "overall_risk_score",
        "overall_risk_level",
        "summary",
        "category_risks",
        "flagged_clauses",
        "missing_standard_protections",
        "recommendations"
    ],
    "additionalProperties": False
}


def analyze_contract(contract_text: str):
    """Analyze a legal contract and return structured JSON."""

    if not contract_text or not contract_text.strip():
        raise ValueError("Contract text is empty.")

    system_prompt = """
You are an AI contract analysis assistant.

Analyze the provided contract carefully.

Your job is to identify:
1. Overall risk level and score.
2. Risks by category.
3. Potentially risky clauses.
4. Missing standard contractual protections.
5. Practical recommendations for reviewing the contract.

Important rules:
- Use ONLY information present in the contract.
- Do not invent clauses.
- Keep original_snippet grounded in the supplied contract.
- Explain legal language in simple language.
- Recommendations are informational and educational, not legal advice.
- Do not claim that a clause is illegal unless the contract text itself clearly establishes that fact.
- Be balanced and explain the reason for each identified risk.
"""

    user_prompt = f"""
Analyze this contract:

---------------- CONTRACT START ----------------

{contract_text}

----------------- CONTRACT END -----------------

Return the analysis using the required JSON structure.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "contract_analysis",
                "schema": ANALYSIS_SCHEMA
            }
        },
        temperature=0.1,
        max_completion_tokens=8000
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty response.")

    try:
        result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Groq returned invalid JSON: {exc}") from exc

    return result


def answer_contract_question(*args, **kwargs):
    """Answer a question using retrieved contract context."""

    question = kwargs.get("question")
    context = kwargs.get("context")

    string_args = [arg for arg in args if isinstance(arg, str)]

    if question is None and string_args:
        question = string_args[-1]

    if context is None and len(string_args) >= 2:
        context = string_args[0]

    if not question:
        raise ValueError("Question is required.")

    if not context:
        context = "No relevant contract sections were retrieved."

    system_prompt = """
You are an AI assistant for contract question answering.

Answer the user's question using ONLY the supplied contract context.

Rules:
- Do not invent information.
- If the answer cannot be found in the supplied context, clearly say so.
- Quote or refer to the relevant contract wording when useful.
- Explain legal language in simple terms.
- This is informational and educational assistance, not legal advice.
"""

    user_prompt = f"""
Contract context:

---------------- CONTEXT START ----------------

{context}

----------------- CONTEXT END -----------------

User question:

{question}

Answer clearly and concisely.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.1,
        max_completion_tokens=2000
    )

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError("Groq returned an empty answer.")

    return answer