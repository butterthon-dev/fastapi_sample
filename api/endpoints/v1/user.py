from typing import List

from fastapi import APIRouter, Request

from api.schemas.user import CreateUser, UpdateUser, UserInDB
from api.v1.user import UserAPI
from migrations.models import User

router = APIRouter()


@router.get('/', response_model=List[UserInDB])
async def gets(request: Request) -> List[User]:
    """ 一覧取得
    """
    return UserAPI.gets(request)


@router.post('/', response_model=UserInDB)
async def create(request: Request, schema: CreateUser) -> User:
    """ 新規登録
    """
    return UserAPI.create(request, schema)


@router.put('/{id}/', response_model=UserInDB)
async def update(request: Request, id: int, schema: UpdateUser) -> User:
    """ 更新
    """
    return UserAPI.update(request, id, schema)


@router.delete('/{id}/')
async def delete(request: Request, id: int) -> None:
    """ 削除
    """
    return UserAPI.delete(request, id)
