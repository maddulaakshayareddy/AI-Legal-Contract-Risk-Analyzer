import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from database.connection import get_db
from models.contract import Contract
from models.user import User
from schemas.contract import ContractCreate, ContractOut
from services.auth_service import get_current_user
from services.authorization_service import get_owned_contract
from services.document_parser import extract_contract_text

router = APIRouter(
    prefix="/api/contracts",
    tags=["Contracts"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/", response_model=ContractOut)
async def create_contract(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    safe_filename = f"{current_user.id}_{Path(file.filename).name}"
    file_path = UPLOAD_DIR / safe_filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        contract_text = extract_contract_text(str(file_path))

        contract = Contract(
            user_id=current_user.id,
            title=title,
            file_name=file.filename,
            file_type=extension.replace(".", ""),
            file_path=str(file_path),
            raw_text=contract_text,
        )

        db.add(contract)
        db.commit()
        db.refresh(contract)

        return contract

    except ValueError as exc:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        if file_path.exists():
            file_path.unlink()

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to process contract: {exc}",
        )

    finally:
        await file.close()


@router.post("/text", response_model=ContractOut)
def create_contract_from_text(
    contract_data: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not contract_data.raw_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Contract text cannot be empty.",
        )

    contract = Contract(
        user_id=current_user.id,
        title=contract_data.title,
        file_name=None,
        file_type="text",
        file_path=None,
        raw_text=contract_data.raw_text,
    )

    db.add(contract)
    db.commit()
    db.refresh(contract)

    return contract


@router.get("/", response_model=list[ContractOut])
def get_my_contracts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Contract)
        .filter(Contract.user_id == current_user.id)
        .order_by(Contract.id.desc())
        .all()
    )


@router.get("/{contract_id}", response_model=ContractOut)
def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_contract(
        contract_id=contract_id,
        db=db,
        current_user=current_user,
    )