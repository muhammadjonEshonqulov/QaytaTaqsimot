from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from app.repositories.student import get_student_by_username, get_user_by_routes
from app.repositories.user import get_user_by_username, create_score
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.response import Response
from app.schemas.user import ScoreSchema
from app.services.auth_service import login_for_access_token
from app.deps.db import get_db, get_current_login

router = APIRouter()


@router.get("/get_students")
async def get_attached_files(db: Session = Depends(get_db), current_user: dict = Depends(get_current_login), ):
    if current_user['role'] != 'user':
        raise HTTPException(status_code=422, detail="Bunday amalni faqat tekshiruvchi amalga oshira oladi")
    else:
        if current_user['login'] is not None:
            _users = get_user_by_routes(db)
            return Response(code=200, success=True, message="success", data=_users).model_dump()
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")



@router.post("/set_score_to_file")
async def set_score_to_file(score: ScoreSchema = Body(), db: Session = Depends(get_db),
                            current_user: dict = Depends(get_current_login)):
    print(current_user['role'])
    if current_user['role'] != 'user':
        raise HTTPException(status_code=422, detail="Bunday amalni faqat tekshiruvchi amalga oshira oladi")
    else:
        if current_user['role'] is not None:
            if 1 <= score.file_number <= 11:
                _score = create_score(db, score)
                return Response(code=200, success=True, message="success", data=_score).model_dump()
            else:
                raise HTTPException(status_code=422, detail="file_number 1 dan 11 gacha bo'lishi kerak")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
