from fastapi import APIRouter, Depends, HTTPException, status, Body, Form, UploadFile
from fastapi.params import File
from sqlalchemy.orm import Session

from app.repositories.student import get_student_by_username, get_user_by_routes
from app.repositories.user import get_user_by_username, create_score, get_score_by_user
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
    if current_user['role'] != 'user':
        raise HTTPException(status_code=422, detail="Bunday amalni faqat tekshiruvchi amalga oshira oladi")

    if not (1 <= score.file_number <= 12):
        raise HTTPException(status_code=422, detail="file_number 1 dan 12 gacha bo'lishi kerak")

    if score.file_number in [1, 2]:
        if not (0 <= score.score <= 20):
            raise HTTPException(status_code=422, detail=f"{score.file_number}-faylga 0 dan 20 gacha ball qo'yilishi kerak")
    elif score.file_number in [3, 5, 7]:
        if not (0 <= score.score <= 10):
            raise HTTPException(status_code=422, detail=f"{score.file_number}-faylga 0 dan 10 gacha ball qo'yilishi kerak")
    elif score.file_number in [4, 6, 8, 9, 10, 11]:
        if not (0 <= score.score <= 5):
            raise HTTPException(status_code=422, detail=f"{score.file_number}-faylga 0 dan 5 gacha ball qo'yilishi kerak")
    elif score.file_number in [12]:
        if not (0 <= score.score <= 80):
            raise HTTPException(status_code=422, detail="Transkript faylga 0 dan 80 gacha ball qo'yilishi kerak")

    _score = create_score(db, score)
    return Response(code=200, success=True, message="success", data=_score).model_dump()


import os
import uuid
from fastapi import UploadFile, File, Form


@router.post("/set_comment_to_student")
async def set_comment_to_student(
        com_comment: str = Form(...),
        student_id_number: str = Form(...),
        com_file: UploadFile = File(...),
        current_user: dict = Depends(get_current_login),
        db: Session = Depends(get_db),
):
    if current_user['role'] != 'user':
        raise HTTPException(status_code=422, detail="Bunday amalni faqat tekshiruvchi amalga oshira oladi")

    _user = get_user_by_username(db, current_user['login'])
    if not _user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    _student = get_student_by_username(db, student_id_number)
    if not _student:
        raise HTTPException(status_code=404, detail="Student topilmadi")

    upload_dir = "files/comments"
    os.makedirs(upload_dir, exist_ok=True)

    file_ext = os.path.splitext(com_file.filename)[1]
    safe_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, safe_filename)

    with open(file_path, "wb") as f:
        f.write(await com_file.read())

    if _user.role == "academic":
        _student.academic_com_note = com_comment
        _student.academic_com_file = file_path
    elif _user.role == "social":
        _student.social_com_note = com_comment
        _student.social_com_file = file_path

    db.commit()
    db.refresh(_student)
    return Response(code=200, success=True, message="success", data={"message": "Izoh va fayl muvaffaqiyatli saqlandi"}).model_dump()
