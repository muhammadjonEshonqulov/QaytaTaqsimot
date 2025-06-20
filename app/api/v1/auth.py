from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.deadline import get_deadline
from app.repositories.student import get_student_by_username
from app.repositories.user import get_user_by_username
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.response import Response
from app.services.auth_service import login_for_access_token
from app.deps.db import get_db, get_current_login
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/login")  # response_model=TokenResponse
def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    token_data = login_for_access_token(db, form_data.login, form_data.password)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parol xato",
        )
    return token_data


@router.get("/me")
async def get_current_user_info(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_login),
):
    role = current_user.get("role")
    user_id = current_user.get("login")
    print(role)
    print(user_id)


    if role == 'student':
        user_data = get_student_by_username(db, user_id)
        deadline = get_deadline(db, 'FILE_UPLOAD')
    elif role == 'user':
        user_data = get_user_by_username(db, user_id)
        deadline = get_deadline(db, 'SCORE')
    else:
        raise HTTPException(status_code=422, detail='Role noto‘g‘ri')

    # Format: string bo'lsa datetime ga o'girish
    start_time = deadline.start_time
    end_time = deadline.end_time

    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    # 5 soat qo‘shish
    start_time_uz = (start_time + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
    end_time_uz = (end_time+ timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")

    deadline2 = {
        "start_time": start_time_uz,
        "end_time": end_time_uz
    }

    if not user_data:
        raise HTTPException(status_code=404, detail='Foydalanuvchi topilmadi')

    user_data_dict = user_data.__dict__.copy()
    user_data_dict['deadline'] = deadline2

    if role == 'student':
        user_data_dict["role"] = role
    return Response(
        code=200, success=True, message="User info", data=user_data_dict
    ).model_dump()
