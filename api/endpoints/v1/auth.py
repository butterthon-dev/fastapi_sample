from fastapi import APIRouter, Depends, Request

from api.v1.auth import AuthAPI
from api.schemas.auth import AuthRequestSchema

router = APIRouter()


@router.post('/login/')
async def login(request: Request, schema: AuthRequestSchema = Depends()):
    """ ログイン
    """
    return AuthAPI.login(request, schema)
