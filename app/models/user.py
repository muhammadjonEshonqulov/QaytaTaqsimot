import datetime
import uuid

from sqlalchemy import Column, Integer, String, ARRAY, DateTime, Boolean, JSON
from app.deps.db import Base
from sqlalchemy.dialects.postgresql.base import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=True)
    surname = Column(String, index=True, nullable=True)
    login = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    role = Column(String, nullable=True)
    created_at = Column(String, default=datetime.datetime.now)
    updated_at = Column(String)


class Student(Base):
    __tablename__ = "students"

    student_id_number = Column(String, primary_key=True)

    first_name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    third_name = Column(String, nullable=True)
    status = Column(String, default="new", nullable=False)
    appeal = Column(Boolean, default=False, nullable=False)
    password = Column(String)
    full_name = Column(String, nullable=True)
    short_name = Column(String, nullable=True)
    image = Column(String, nullable=True)
    birth_date = Column(Integer, nullable=True)
    social_score = Column(Integer, nullable=True)
    academic_score = Column(Integer, nullable=True)
    passport_pin = Column(String, nullable=True)
    passport_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    academic_com_note = Column(String, nullable=True)
    academic_app_note = Column(String, nullable=True)
    academic_com_file = Column(String, nullable=True)
    academic_app_file = Column(String, nullable=True)
    social_com_note = Column(String, nullable=True)
    social_app_note = Column(String, nullable=True)
    social_com_file = Column(String, nullable=True)
    social_app_file = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    university = Column(String, nullable=True)
    address = Column(String, nullable=True)
    validateUrl = Column(String, nullable=True)
    hash = Column(String, nullable=True)
    file_number1 = Column(String, nullable=True)
    file_number2 = Column(String, nullable=True)
    file_number3 = Column(String, nullable=True)
    file_number4 = Column(String, nullable=True)
    file_number5 = Column(String, nullable=True)
    file_number6 = Column(String, nullable=True)
    file_number7 = Column(String, nullable=True)
    file_number8 = Column(String, nullable=True)
    file_number9 = Column(String, nullable=True)
    file_number10 = Column(String, nullable=True)
    file_number11 = Column(String, nullable=True)
    file_number12 = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    password_valid = Column(Boolean, nullable=True)
    gender = Column(JSON, nullable=True)
    specialty = Column(JSON, nullable=True)
    studentStatus = Column(JSON, nullable=True)
    educationForm = Column(JSON, nullable=True)
    educationType = Column(JSON, nullable=True)
    paymentForm = Column(JSON, nullable=True)
    group = Column(JSON, nullable=True)
    faculty = Column(JSON, nullable=True)
    educationLang = Column(JSON, nullable=True)
    level = Column(JSON, nullable=True)
    semester = Column(JSON, nullable=True)
    country = Column(JSON, nullable=True)
    province = Column(JSON, nullable=True)
    district = Column(JSON, nullable=True)
    socialCategory = Column(JSON, nullable=True)
    accommodation = Column(JSON, nullable=True)


class Scores(Base):
    __tablename__ = "scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id_number = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    file_number = Column(Integer, nullable=True)
    file_url = Column(String, nullable=True)
    checker_id = Column(UUID, nullable=True)
    created_at = Column(String, default=datetime.datetime.now)
    updated_at = Column(String)

    class Config:
        orm_mode = True
