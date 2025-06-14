from datetime import timedelta, datetime
import requests

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.repositories.student import create_student, get_student_by_username
from app.repositories.user import get_user_by_username
from app.schemas.student import StudentInfoSchema


def login_for_access_token(db: Session, username: str, password: str):
    if username.startswith('user_'):
        user = authenticate_user(db, username, password)
        if not user:
            return None
        token = create_access_token(data={"login": user.login, "role": "user"})
        return {"role": user.role, "access_token": token}
    return student_login_flow(db, username, password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def student_login_flow(db: Session, login: str, password: str):
    _student = get_student_by_username(db, student_id=login)

    # Agar student mavjud emas yoki updated_at eski bo‘lsa → remote tekshiruv
    if not _student or not _student.updated_at or ((datetime.now().date() - _student.updated_at.date()).days >= 1):
        remote_login_url = "https://student.jbnuu.uz/rest/v1/auth/login"
        remote_me_url = "https://student.jbnuu.uz/rest/v1/account/me"
        remote_gpa_url = "https://student.jbnuu.uz/rest/v1/education/gpa-list"

        remote_login_payload = {"login": login, "password": password}
        r_login = requests.post(remote_login_url, json=remote_login_payload, timeout=10)

        if r_login.status_code != 200:
            return None

        remote_data = r_login.json()
        remote_token = remote_data.get("data", {}).get("token")
        if not remote_token:
            raise HTTPException(status_code=500, detail="Token topilmadi (remote)")

        # Remote token orqali student ma'lumotlarini olish
        headers = {"Authorization": f"Bearer {remote_token}"}
        r_me = requests.get(remote_me_url, headers=headers, timeout=10)
        if r_me.status_code != 200:
            raise HTTPException(status_code=401, detail="ME ma'lumotini olishda xatolik")

        me_data = r_me.json().get("data")
        try:
            student_info = StudentInfoSchema(**me_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Remote data parsing error: {e}")

        if not (
                student_info.educationForm.name == 'Kunduzgi' and student_info.educationType.name == 'Bakalavr' and student_info.level.name == '1-kurs' and student_info.studentStatus.name == 'O‘qimoqda'):
            raise HTTPException(status_code=422, detail='Talaba 1-kurs Bakalavr Kunduzgi bo‘lishi kerak va O‘qiyotgan bo‘lishi kerak')

        r_gpa = requests.get(remote_gpa_url, headers=headers, timeout=10)
        if r_gpa.status_code != 200:
            raise HTTPException(status_code=401, detail="GPA ma'lumotini olishda xatolik")

        gpa_data = r_gpa.json().get("data")
        for gpa in gpa_data:
            if gpa['educationYear']['current']:
                student_info.gpa = gpa['gpa']
                break
        if not student_info.gpa or (student_info.gpa < '3.5'):
            raise HTTPException(status_code=422, detail=f'Sizning GPA eng kamida 3.5 bo‘lishi kerak. Sizning GPA: {student_info.gpa if student_info.gpa is not None else "Mavjud emas"}')
        # Bazaga yozish
        _student = create_student(db, student_info, password)

    # Lokal parol tekshiruvi
    if not verify_password(plain_password=password, hashed_password=_student.password):
        return None

    token = create_access_token(
        data={"login": _student.student_id_number, "role": "student"},
        expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
    )

    return {"role": "student", "access_token": token}
