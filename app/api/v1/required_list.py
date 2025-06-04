from fastapi import APIRouter, Depends
from requests import Session

from app.deps.db import get_db
from app.repositories.required_list import get_list
from app.schemas.response import Response

router = APIRouter()


@router.get("/get_required_list")
async def get_required_list(
        db: Session = Depends(get_db),
):
    _list = get_list(db)
    return Response(
        code=200, success=True, message="success", data=_list
    ).model_dump()
