from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CodeNameModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class SpecialtyModel(BaseModel):
    id: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class EducationLangModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class GroupModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    educationLang: Optional[EducationLangModel] = None

    class Config:
        from_attributes = True


class StructureTypeModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class LocalityTypeModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class FacultyModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    structureType: Optional[StructureTypeModel] = None
    localityType: Optional[LocalityTypeModel] = None
    parent: Optional[str] = None
    active: Optional[bool] = None

    class Config:
        from_attributes = True


class LevelModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class EducationYearModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    current: Optional[bool] = None

    class Config:
        from_attributes = True


class SemesterModel(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None
    current: Optional[bool] = None
    education_year: Optional[EducationYearModel] = None

    class Config:
        from_attributes = True


class CountryModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class ProvinceModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    parent_: Optional[str] = Field(None, alias="_parent")

    class Config:
        from_attributes = True
        populate_by_name = True


class DistrictModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    parent_: Optional[str] = Field(None, alias="_parent")

    class Config:
        from_attributes = True
        populate_by_name = True


class SocialCategoryModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class AccommodationModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class StudentInfoSchema(BaseModel):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    third_name: Optional[str] = None
    full_name: Optional[str] = None
    short_name: Optional[str] = None
    password: Optional[str] = None
    student_id_number: Optional[str] = None
    image: Optional[str] = None
    birth_date: Optional[int] = None
    passport_pin: Optional[str] = None
    passport_number: Optional[str] = None
    email: Optional[str] = None
    file_number1: Optional[str] = None
    file_number2: Optional[str] = None
    file_number3: Optional[str] = None
    file_number4: Optional[str] = None
    file_number5: Optional[str] = None
    file_number6: Optional[str] = None
    file_number7: Optional[str] = None
    file_number8: Optional[str] = None
    file_number9: Optional[str] = None
    file_number10: Optional[str] = None
    file_number11: Optional[str] = None
    file_number12: Optional[str] = None

    phone: Optional[str] = None
    gender: Optional[CodeNameModel] = None
    university: Optional[str] = None
    specialty: Optional[SpecialtyModel] = None
    studentStatus: Optional[CodeNameModel] = None
    educationForm: Optional[CodeNameModel] = None
    educationType: Optional[CodeNameModel] = None
    paymentForm: Optional[CodeNameModel] = None
    group: Optional[GroupModel] = None
    faculty: Optional[FacultyModel] = None
    educationLang: Optional[CodeNameModel] = None
    level: Optional[LevelModel] = None
    semester: Optional[SemesterModel] = None
    password_valid: Optional[bool] = None
    address: Optional[str] = None
    country: Optional[CountryModel] = None
    province: Optional[ProvinceModel] = None
    district: Optional[DistrictModel] = None
    socialCategory: Optional[SocialCategoryModel] = None
    accommodation: Optional[AccommodationModel] = None
    validateUrl: Optional[str] = None
    hash: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True
