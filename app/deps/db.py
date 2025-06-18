from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.security import SECRET_KEY, ALGORITHM
from app.deps.base_class import Base
from app.repositories.required_list import seed_required_list

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


DATABASE_URL = "postgresql://myuser:myPassword@pgsql:5432/qayta_taqsimot"

# Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """DB yaratish va default qiymatlarni qo‘shish."""
    try:
        Base.metadata.create_all(bind=engine)  # Jadvalni yaratish
        db = SessionLocal()

        seed_required_list(db)
        db.close()
    except Exception as e:
        print(f"Ma'lumotlar bazasini sozlashda xato: {e}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def get_current_login(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print('payload', payload)
        user_id: str = payload.get("login")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
        return {"login": user_id, "role": role}
    except JWTError:
        raise credentials_exception
