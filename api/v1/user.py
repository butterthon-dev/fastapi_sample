from api.schemas.user import CreateUser, UpdateUser, UserInDB
from crud.crud_user import CRUDUser
from fastapi import Request
# from fastapi.encoders import jsonable_encoder  # 削除
from typing import List


class UserAPI:
    """ ユーザーに関するAPI
    """
    @classmethod
    def gets(cls, request: Request) -> List[UserInDB]:
        """ 一覧取得
        """
        return CRUDUser(request.state.db_session).gets()  # jsonable_encoderは使わない

    @classmethod
    def create(
        cls,
        request: Request,
        schema: CreateUser
    ) -> UserInDB:
        """ 新規登録
        """
        return CRUDUser(request.state.db_session).create(schema.dict())

    @classmethod
    def update(
        cls,
        request: Request,
        id: int,
        schema: UpdateUser
    ) -> UserInDB:
        """ 更新
        """
        crud = CRUDUser(request.state.db_session)
        obj = crud.get_by_id(id)
        return CRUDUser(request.state.db_session).update(obj, schema.dict())

    @classmethod
    def delete(cls, request: Request, id: int) -> None:
        """ 削除
        """
        return CRUDUser(request.state.db_session).delete_by_id(id)
