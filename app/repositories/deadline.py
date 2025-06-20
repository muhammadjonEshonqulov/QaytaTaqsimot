
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.deadline import Deadlines
from app.models.user import User, Student, Scores
from app.schemas.user import ScoreSchema


def get_deadline(db: Session, deadline_type: str):
    return db.query(Deadlines).filter(Deadlines.deadline_type == deadline_type).first()