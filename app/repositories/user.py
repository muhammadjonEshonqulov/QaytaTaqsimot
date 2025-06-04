import datetime
from operator import and_

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.deadline import Deadlines
from app.models.user import User, Student, Scores
from app.schemas.user import ScoreSchema


def get_user_by_username(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()

def create_score(db: Session, score: ScoreSchema):
    _deadline = db.query(Deadlines).filter(Deadlines.deadline_type == 'SCORE').order_by(desc(Deadlines.created_at)).first()

    if not _deadline or datetime.datetime.strptime(_deadline.start_time, "%Y-%m-%d %H:%M:%S") > datetime.datetime.now():
        raise HTTPException(
            status_code=422,
            detail="Baxolashga hali ruxsat berilmagan"
        )

    elif datetime.datetime.strptime(_deadline.end_time, "%Y-%m-%d %H:%M:%S") < datetime.datetime.now():
        raise HTTPException(
            status_code=422,
            detail="Baxolash tugatilgan"
        )
    else:
        existing_score = db.query(Scores).filter(
            and_(
                Scores.student_id_number == score.student_id_number,
                Scores.file_number == score.file_number
            )
        ).first()

        if not existing_score:
            _score = Scores(
                student_id_number=score.student_id_number,
                file_number=score.file_number,
                score=score.score,
                file_url=score.file_url,
                checker_id=score.checker_id,
                created_at=str(datetime.datetime.now()),
            )
            db.add(_score)
            db.commit()
            db.refresh(_score)
            return _score

        else:
            score.updated_at = str(datetime.datetime.now())

            update_data = score.model_dump(exclude_unset=True)
            for field_name, field_value in update_data.items():
                setattr(existing_score, field_name, field_value)

            db.commit()
            db.refresh(existing_score)
            return existing_score
