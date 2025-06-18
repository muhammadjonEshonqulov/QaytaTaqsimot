from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from sqlalchemy.testing.suite.test_reflection import users
from starlette.staticfiles import StaticFiles

from app.api.v1 import auth, student, user
from app.deps.db import init_db

# DB ni boshlang'ich sozlash
init_db()

app = FastAPI()

# Define allowed origins (adjust for production)
origins = [
    "http://127.0.0.1:5500",  # your frontend origin (e.g., VS Code Live Server)
    "http://localhost:5500",   # optional for local testing
    "https://qayta-taqsimot.vercel.app", # Vercel'dagi frontend domeni
    "https://grantlar-taqsimoti.jbnuu.uz",  # add production origin if needed
]

app.mount("/my_files", StaticFiles(directory="my_files"), name="my_files")
app.mount("/profile_images", StaticFiles(directory="profile_images"), name="profile_images")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],              # allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],              # allow all headers
)

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global xato handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal Server Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)}
    )

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(student.router, prefix="/api/v1/student", tags=["student"])
app.include_router(user.router, prefix="/api/v1/user", tags=["student"])

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)