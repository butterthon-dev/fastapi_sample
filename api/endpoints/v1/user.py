from api.schemas.user import CreateUser, UpdateUser, UserInDB
from api.v1.user import UserAPI
from dependencies import set_db_session_in_request
from fastapi import APIRouter, Depends, Request
from typing import List

router = APIRouter()


@router.get(
    '/',
    response_model=List[UserInDB],  # response_modelを追加
    dependencies=[Depends(set_db_session_in_request)])
async def gets(request: Request) -> List[UserInDB]:
    """ 一覧取得
    """
    return UserAPI.gets(request)


@router.post(
    '/',
    response_model=UserInDB,
    dependencies=[Depends(set_db_session_in_request)])
async def create(request: Request, schema: CreateUser) -> UserInDB:
    """ 新規登録
    """
    return UserAPI.create(request, schema)


@router.put(
    '/{id}/',
    response_model=UserInDB,
    dependencies=[Depends(set_db_session_in_request)])
async def update(request: Request, id: int, schema: UpdateUser) -> UserInDB:
    """ 更新
    """
    return UserAPI.update(request, id, schema)


@router.delete(
    '/{id}/',
    dependencies=[Depends(set_db_session_in_request)])
async def delete(request: Request, id: int) -> None:
    """ 削除
    """
    return UserAPI.delete(request, id)
