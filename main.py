from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.testing.suite.test_reflection import users

from app.api.v1 import auth, student, user
from app.deps.db import init_db

# DB ni boshlang'ich sozlash
init_db()

app = FastAPI()

# Define allowed origins (adjust for production)
origins = [
    "http://127.0.0.1:5500",  # your frontend origin (e.g., VS Code Live Server)
    "http://localhost:5500",   # optional for local testing
    # "https://yourdomain.com",  # add production origin if needed
]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],              # allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],              # allow all headers
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

app.include_router(student.router, prefix="/api/v1/student", tags=["student"])
app.include_router(user.router, prefix="/api/v1/user", tags=["student"])
