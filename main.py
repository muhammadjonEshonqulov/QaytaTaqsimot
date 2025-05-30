from fastapi import FastAPI
from app.api.v1 import auth, student
from app.deps.db import init_db

init_db()

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(student.router, prefix="/api/v1/student", tags=["student"])
