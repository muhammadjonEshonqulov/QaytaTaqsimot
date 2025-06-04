from sqlalchemy import Column, Integer, String

from app.deps.db import Base


class RequiredList(Base):
    __tablename__ = "required_list"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
