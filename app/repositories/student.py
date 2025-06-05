import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import Student, Scores
from app.repositories.required_list import get_list
from app.schemas.student import StudentInfoSchema


def get_student_by_username(db: Session, student_id: str):
    return db.query(Student).filter(Student.student_id_number == student_id).first()


def get_user_by_routes(db: Session):
    _students = db.query(Student).all()
    _scores = db.query(Scores).all()

    # Build lookup table: (student_id_number, file_number as str) => score
    score_lookup = {
        (score.student_id_number, str(score.file_number)): score.score
        for score in _scores
    }

    required_list = get_list(db)

    students = []
    for student in _students:
        files = []

        for file in required_list:
            file_attr_name = f'file_number{file.id}'
            file_number_value = getattr(student, file_attr_name, None)

            # if file_number_value is not None:
            key = (student.student_id_number, str(file.id))
            score = score_lookup.get(key)

            # Optionally store this dynamically on the student object
            setattr(student, f'{file_attr_name}_score', score)

            files.append({
                "id": file.id,
                "name": file.name,
                "file_url": file_number_value,
                "score": score
            })
        files.append({
            "id": 12,
            "name": 'Transkript',
            "file_url": student.file_number12,
            "score": score_lookup.get((student.student_id_number, str(12)))
        })
        student_data = {
            "short_name": student.short_name,
            "student_id_number": student.student_id_number,
            "status": student.status,
            "appeal": student.appeal,
            "files": files
        }

        students.append(student_data)

    return students


def get_students(db: Session):
    return db.query(Student).all()


def update_student(db: Session, student_id_number: str, file_url: str, file_number: int):
    """Update the student's file URL in the database."""
    _student = get_student_by_username(db=db, student_id=student_id_number)
    if not _student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Ensure file_number is in the valid range
    if file_number < 1 or file_number > 12:
        raise HTTPException(status_code=400, detail="file_number must be between 1 and 12")

    # Determine which file number field to update
    file_field = f"file_number{file_number}"

    # Ensure the column exists in the student model
    if not hasattr(_student, file_field):
        raise HTTPException(status_code=400, detail=f"Invalid file number: {file_number}")

    setattr(_student, file_field, file_url)  # Update the field with the file URL

    db.commit()
    db.refresh(_student)
    return _student


def create_student(db: Session, student: StudentInfoSchema, password: str):
    existing_student = db.query(Student).filter(
        Student.student_id_number == student.student_id_number
    ).first()
    if existing_student:
        # Mavjud bo‘lsa, update qilish
        print('student.file_number1', student.file_number1)

        existing_student.first_name = student.first_name
        existing_student.second_name = student.second_name
        existing_student.third_name = student.third_name
        existing_student.full_name = student.full_name
        existing_student.short_name = student.short_name
        existing_student.image = student.image
        existing_student.university = student.university
        existing_student.birth_date = student.birth_date
        existing_student.password = get_password_hash(password)
        existing_student.passport_pin = student.passport_pin
        existing_student.passport_number = student.passport_number
        existing_student.email = student.email
        existing_student.phone = student.phone
        if student.file_number1 is not None:
            print('existing_student.file_number1', existing_student.file_number1)
            existing_student.file_number1 = student.file_number1
            print('existing_student.file_number1', existing_student.file_number1)
        if student.file_number2 is not None:
            existing_student.file_number2 = student.file_number2
        if student.file_number3 is not None:
            existing_student.file_number3 = student.file_number3
        if student.file_number4 is not None:
            existing_student.file_number4 = student.file_number4
        if student.file_number5 is not None:
            existing_student.file_number5 = student.file_number5
        if student.file_number6 is not None:
            existing_student.file_number6 = student.file_number6
        if student.file_number7 is not None:
            existing_student.file_number7 = student.file_number7
        if student.file_number8 is not None:
            existing_student.file_number8 = student.file_number8
        if student.file_number9 is not None:
            existing_student.file_number9 = student.file_number9
        if student.file_number10 is not None:
            existing_student.file_number10 = student.file_number10
        if student.file_number11 is not None:
            existing_student.file_number11 = student.file_number11,
        if student.file_number12 is not None:
            existing_student.file_number12 = student.file_number12

        existing_student.address = student.address
        existing_student.validateUrl = student.validateUrl
        existing_student.hash = student.hash
        existing_student.password_valid = student.password_valid
        existing_student.gender = student.gender.model_dump() if student.gender else None
        existing_student.specialty = student.specialty.model_dump() if student.specialty else None
        existing_student.studentStatus = student.studentStatus.model_dump() if student.studentStatus else None
        existing_student.educationForm = student.educationForm.model_dump() if student.educationForm else None
        existing_student.educationType = student.educationType.model_dump() if student.educationType else None
        existing_student.paymentForm = student.paymentForm.model_dump() if student.paymentForm else None
        existing_student.group = student.group.model_dump() if student.group else None
        existing_student.faculty = student.faculty.model_dump() if student.faculty else None
        existing_student.educationLang = student.educationLang.model_dump() if student.educationLang else None
        existing_student.level = student.level.model_dump() if student.level else None
        existing_student.semester = student.semester.model_dump() if student.semester else None
        existing_student.country = student.country.model_dump() if student.country else None
        existing_student.province = student.province.model_dump() if student.province else None
        existing_student.district = student.district.model_dump() if student.district else None
        existing_student.socialCategory = student.socialCategory.model_dump() if student.socialCategory else None
        existing_student.accommodation = student.accommodation.model_dump() if student.accommodation else None
        existing_student.updated_at = datetime.datetime.now()

        db.commit()
        db.refresh(existing_student)
        return existing_student

    else:
        # Yo‘q bo‘lsa, create qilish
        new_student = Student(
            first_name=student.first_name,
            second_name=student.second_name,
            third_name=student.third_name,
            full_name=student.full_name,
            password=get_password_hash(password),
            short_name=student.short_name,
            student_id_number=student.student_id_number,
            image=student.image,
            university=student.university,
            birth_date=student.birth_date,
            passport_pin=student.passport_pin,
            file_number1=student.file_number1,
            file_number2=student.file_number2,
            file_number3=student.file_number3,
            file_number4=student.file_number4,
            file_number5=student.file_number5,
            file_number6=student.file_number6,
            file_number7=student.file_number7,
            file_number8=student.file_number8,
            file_number9=student.file_number9,
            file_number10=student.file_number10,
            file_number11=student.file_number11,
            passport_number=student.passport_number,
            email=student.email,
            phone=student.phone,
            address=student.address,
            validateUrl=student.validateUrl,
            hash=student.hash,
            password_valid=student.password_valid,
            gender=student.gender.model_dump() if student.gender else None,
            specialty=student.specialty.model_dump() if student.specialty else None,
            studentStatus=student.studentStatus.model_dump() if student.studentStatus else None,
            educationForm=student.educationForm.model_dump() if student.educationForm else None,
            educationType=student.educationType.model_dump() if student.educationType else None,
            paymentForm=student.paymentForm.model_dump() if student.paymentForm else None,
            group=student.group.model_dump() if student.group else None,
            faculty=student.faculty.model_dump() if student.faculty else None,
            educationLang=student.educationLang.model_dump() if student.educationLang else None,
            level=student.level.model_dump() if student.level else None,
            semester=student.semester.model_dump() if student.semester else None,
            country=student.country.model_dump() if student.country else None,
            province=student.province.model_dump() if student.province else None,
            district=student.district.model_dump() if student.district else None,
            socialCategory=student.socialCategory.model_dump() if student.socialCategory else None,
            accommodation=student.accommodation.model_dump() if student.accommodation else None,
            created_at=datetime.datetime.now(),
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

    return new_student
