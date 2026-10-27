from typing import Optional

from pydantic import BaseModel


class ContractCreate(BaseModel):
    title: str
    raw_text: str


class ContractOut(BaseModel):
    id: int
    user_id: int
    title: str
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    raw_text: str

    class Config:
        from_attributes = True