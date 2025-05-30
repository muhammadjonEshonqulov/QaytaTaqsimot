import datetime
import uuid

from sqlalchemy import Column, String, UUID

from app.deps.db import Base


class Deadlines(Base):
    __tablename__ = "deadlines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deadline_type = Column(String, nullable=True)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)
    admin_id = Column(String, nullable=True)
    created_at = Column(String, default=datetime.datetime.now)