from api.v1.auth import AuthAPI
from dependencies import set_db_session_in_request
from fastapi import APIRouter, Depends, Request

router = APIRouter()


@router.post(
    '/login/',
    dependencies=[Depends(set_db_session_in_request)])
async def gets(request: Request):
    """ ログイン
    """
    return AuthAPI.login(request)
