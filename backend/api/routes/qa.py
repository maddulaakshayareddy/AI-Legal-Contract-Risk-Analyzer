from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from models.qa import Question
from models.user import User
from schemas.qa import QuestionCreate, QuestionOut
from services.auth_service import get_current_user
from services.authorization_service import get_owned_contract
from services.rag_service import build_rag_context
from services.gemini_service import answer_contract_question


router = APIRouter(
    prefix="/api/qa",
    tags=["Contract Q&A"]
)


@router.post("/", response_model=QuestionOut)
def ask_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify that the contract belongs to the logged-in user.
    contract = get_owned_contract(
        contract_id=question_data.contract_id,
        db=db,
        current_user=current_user
    )

    context = build_rag_context(
        question_data.question,
        contract.raw_text
    )

    try:
        answer = answer_contract_question(
            question=question_data.question,
            context=context
        )

        question = Question(
            contract_id=contract.id,
            user_id=current_user.id,
            question_text=question_data.question,
            answer_text=answer,
            retrieved_snippets=context
        )

        db.add(question)
        db.commit()
        db.refresh(question)

        return question

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to answer question: {exc}"
        )