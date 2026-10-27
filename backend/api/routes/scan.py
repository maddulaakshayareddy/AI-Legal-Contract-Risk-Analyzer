import os
import uuid
from io import BytesIO

import numpy as np
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from database.connection import get_db
from models.contract import Contract
from models.user import User
from services.auth_service import get_current_user


router = APIRouter(
    prefix="/api/scan",
    tags=["Scan & OCR"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

_reader = None


def get_ocr_reader():
    global _reader

    if _reader is None:
        import easyocr

        _reader = easyocr.Reader(
            ["en"],
            gpu=False,
            verbose=False
        )

    return _reader


@router.post("/upload")
async def upload_scanned_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Scan upload expects an image such as JPG, PNG, or WEBP.",
        )

    raw_bytes = await file.read()

    if not raw_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded scan is empty.",
        )

    try:
        image = Image.open(
            BytesIO(raw_bytes)
        ).convert("RGB")

    except (
        UnidentifiedImageError,
        OSError,
    ) as exc:

        raise HTTPException(
            status_code=400,
            detail="The uploaded scan could not be read as an image.",
        ) from exc

    stored_name = (
        f"{uuid.uuid4().hex}_"
        f"{file.filename or 'scan.jpg'}"
    )

    stored_path = os.path.join(
        UPLOAD_DIR,
        stored_name
    )

    with open(
        stored_path,
        "wb"
    ) as output:

        output.write(raw_bytes)

    try:
        reader = get_ocr_reader()

        image_array = np.array(image)

        text_parts = reader.readtext(
            image_array,
            detail=0,
            paragraph=True
        )

        extracted_text = "\n\n".join(
            part.strip()
            for part in text_parts
            if part and part.strip()
        ).strip()

    except Exception as exc:

        if os.path.exists(stored_path):
            os.remove(stored_path)

        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(exc)}",
        ) from exc

    if len(extracted_text) < 10:

        if os.path.exists(stored_path):
            os.remove(stored_path)

        raise HTTPException(
            status_code=422,
            detail=(
                "The scan did not contain enough readable text. "
                "Please capture the page more clearly."
            ),
        )

    contract = Contract(
        user_id=current_user.id,
        title=title.strip() or "Scanned Contract",
        file_name=file.filename or stored_name,
        file_type="scan",
        file_path=stored_path,
        raw_text=extracted_text,
    )

    db.add(contract)
    db.commit()
    db.refresh(contract)

    return {
        "id": contract.id,
        "title": contract.title,
        "file_name": contract.file_name,
        "file_type": contract.file_type,
        "message": (
            "Scan uploaded and OCR text extracted successfully."
        ),
    }