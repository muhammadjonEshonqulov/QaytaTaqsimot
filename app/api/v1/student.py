import datetime
import os
import shutil
import uuid

# students/router.py
from fastapi import APIRouter, File, UploadFile
from fastapi import Depends, Request
from fastapi import Form, HTTPException
from requests import Session
from sqlalchemy import desc

from app.deps.db import get_db, get_current_login
from app.models.deadline import Deadlines
from app.repositories.student import get_student_by_username, get_students, update_student
from app.schemas.response import Response

router = APIRouter()

UPLOAD_DIR_IMAGES = "profile_images"
UPLOAD_DIR_FILES = "my_files"
os.makedirs(UPLOAD_DIR_FILES, exist_ok=True)
os.makedirs(UPLOAD_DIR_IMAGES, exist_ok=True)


@router.delete("/file_delete")
async def delete_file(file_number: int = Form(...),
                      db: Session = Depends(get_db),
                      current_student: dict = Depends(get_current_login),
                      ):
    if current_student['role'] != 'student':
        raise HTTPException(status_code=422, detail="Bunday amalni faqat talaba amalga oshira oladi")

    _deadline = db.query(Deadlines).filter(Deadlines.deadline_type == 'FILE_UPLOAD').order_by(
        desc(Deadlines.created_at)).first()

    if not _deadline or datetime.datetime.strptime(_deadline.start_time, "%Y-%m-%d %H:%M:%S") > datetime.datetime.now():
        raise HTTPException(
            status_code=422,
            detail="Fayl o'zgartirishga hali ruxsat berilmagan"
        )

    elif datetime.datetime.strptime(_deadline.end_time, "%Y-%m-%d %H:%M:%S") < datetime.datetime.now():
        raise HTTPException(
            status_code=422,
            detail="Fayl o'zgartirish tugatilgan"
        )
    else:
        if not file_number:
            raise HTTPException(status_code=400, detail="file_number is required")
        student_id = current_student["login"]
        updated_student = update_student(db=db, student_id_number=student_id, file_url=None, file_number=file_number)
        return {
            "file_number": file_number,
            "your_files": {
                'file_number1': updated_student.file_number1,
                'file_number2': updated_student.file_number2,
                'file_number3': updated_student.file_number3,
                'file_number4': updated_student.file_number4,
                'file_number5': updated_student.file_number5,
                'file_number6': updated_student.file_number6,
                'file_number7': updated_student.file_number7,
                'file_number8': updated_student.file_number8,
                'file_number9': updated_student.file_number9,
                'file_number10': updated_student.file_number10,
                'file_number11': updated_student.file_number11,
                'file_number12': updated_student.file_number12
            }
        }


@router.post("/upload")
async def create_upload_files(
        file_number: int = Form(...),
        file: UploadFile = File(...),
        current_student: dict = Depends(get_current_login),
        db: Session = Depends(get_db),  # Ensure DB session is injected
):
    if current_student['role'] != 'student':
        raise HTTPException(status_code=422, detail="Bunday amalni faqat talaba amalga oshira oladi")
    student_id = current_student["login"]

    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="File not uploaded!")

    _deadline = db.query(Deadlines).filter(Deadlines.deadline_type == 'FILE_UPLOAD').order_by(
        desc(Deadlines.created_at)).first()

    if not _deadline or datetime.datetime.strptime(_deadline.start_time, "%Y-%m-%d %H:%M:%S") > datetime.datetime.now():
        raise HTTPException(
            status_code=422,
            detail="Fayl yuklashga hali ruxsat berilmagan"
        )

    elif datetime.datetime.strptime(_deadline.end_time, "%Y-%m-%d %H:%M:%S") < datetime.datetime.now():
        raise HTTPException(
            status_code=422,
            detail="Fayl yuklash tugatilgan"
        )
    else:
        file_extension = file.filename.split(".")[-1]  # Extract file extension
        file_name_raw = ".".join(file.filename.split(".")[:-1]).strip()  # Get file name without extension
        file_name = file_name_raw[-5:] if len(file_name_raw) >= 5 else file_name_raw  # Keep last 5 characters
        # Define file path for saving
        file_path = f"{UPLOAD_DIR_FILES}/{student_id}_{file_number}_{file_name}.{file_extension}"

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Generate file URL (assuming local storage; update based on your setup)
        file_url = f"/my_files/{student_id}_{file_number}_{file_name}.{file_extension}"

        # Update student record with the file URL
        updated_student = update_student(db=db, student_id_number=student_id, file_url=file_url,
                                         file_number=file_number)

        return {
            "file_number": file_number,
            "saved_file": file_url,
            "your_files": {
                'file_number1': updated_student.file_number1,
                'file_number2': updated_student.file_number2,
                'file_number3': updated_student.file_number3,
                'file_number4': updated_student.file_number4,
                'file_number5': updated_student.file_number5,
                'file_number6': updated_student.file_number6,
                'file_number7': updated_student.file_number7,
                'file_number8': updated_student.file_number8,
                'file_number9': updated_student.file_number9,
                'file_number10': updated_student.file_number10,
                'file_number11': updated_student.file_number11,
                'file_number12': updated_student.file_number12
            }
        }


@router.get("/student-me")
async def get_student_by_id_route(
        db: Session = Depends(get_db),
        current_student: dict = Depends(get_current_login),
):
    _student = get_student_by_username(db, current_student["login"])
    return Response(
        code=200, success=True, message="success", data=_student
    ).model_dump()


@router.get("/get_student/{student_id}")
async def get_student_by_id_route(
        student_id: uuid.UUID,
        db: Session = Depends(get_db),
        _=Depends(get_current_login),
):
    _student = get_student_by_username(db, student_id)
    return Response(code=200, success=True, message="success", data=_student).model_dump()


#
#
@router.get("/get_students")
async def get_students_route(
        req: Request,
        db: Session = Depends(get_db),
        _=Depends(get_current_login),
):
    _students = get_students(db)
    return Response(
        code=200,
        success=True,
        message="success",
        data=_students
        ,
    ).model_dump()


@router.post("/appeal")
async def set_appeal(
        app_comment: str = Form(...),
        app_file: UploadFile = File(...),
        current_user: dict = Depends(get_current_login),
        db: Session = Depends(get_db),
):
    if current_user['role'] != 'student':
        raise HTTPException(status_code=422, detail="Bunday amalni faqat talaba amalga oshira oladi")

    _student = get_student_by_username(db, current_user['login'])
    if not _student:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")

    upload_dir = "files/appeals"
    os.makedirs(upload_dir, exist_ok=True)

    file_ext = os.path.splitext(app_file.filename)[1]
    safe_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, safe_filename)

    with open(file_path, "wb") as f:
        f.write(await app_file.read())


    _student.app_com = app_comment
    _student.app_file = file_path


    db.commit()
    db.refresh(_student)
    return Response(code=200, success=True, message="success", data={"message": "Apelatsiyaga izoh va fayl muvaffaqiyatli saqlandi"}).model_dump()

#
# @router.get("/get_students_with_scores")
# async def get_students_with_scores_route(
#         db: Session = Depends(get_db),
#         # _=Depends(get_current_login),
# ):
#     _students = get_students_with_scores(db)
#     return Response(
#         code=200,
#         success=True,
#         message="success",
#         data=_students
#         ,
#     ).model_dump()
