from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.student import get_student_by_username
from app.repositories.user import get_user_by_username
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.response import Response
from app.services.auth_service import login_for_access_token
from app.deps.db import get_db, get_current_login

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    token_data = login_for_access_token(db, form_data.login, form_data.password)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
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
    elif role == 'user':
        user_data = get_user_by_username(db, user_id)
    else:
        raise HTTPException(status_code=422, detail='Role noto‘g‘ri')

    if not user_data:
        raise HTTPException(status_code=404, detail='Foydalanuvchi topilmadi')

    return Response(
        code=200, success=True, message="User info", data=user_data
    ).model_dump()
