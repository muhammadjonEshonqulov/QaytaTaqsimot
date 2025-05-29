from sqlalchemy.orm import Session
from app.models.user import User, Student


def get_user_by_username(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()

