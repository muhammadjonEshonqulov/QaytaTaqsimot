import uuid
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Numeric


class ScoreSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    student_id_number: str = None
    score: Optional[Decimal] = None
    file_number: int = None
    file_url: str = None
    checker_id: uuid.UUID = None
    updated_at: Optional[str] = None
    created_at: Optional[str] = None
