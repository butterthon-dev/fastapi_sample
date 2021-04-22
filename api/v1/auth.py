from typing import Dict

from fastapi import Request

from api.schemas.auth import AuthRequestSchema
from crud.crud_user import CRUDUser
from exceptions import ApiException, create_error
from exceptions.error_messages import ErrorMessage
from migrations.models import User
from utilities.hasher import check_password
from utilities.jwt_handler import (
    jwt_claims_handler,
    jwt_encode_handler,
    jwt_response_handler,
    TYPE_ACCESS_TOKEN,
)


class AuthAPI:
    """ 認証に関するAPI
    """
    @classmethod
    def login(
        cls,
        request: Request,
        schema: AuthRequestSchema
    ) -> Dict[str, str]:
        """ ログインAPI

        Args:
            request (Request): リクエスト情報
            schema (AuthRequestSchema): リクエストボディ

        Returns:
            Dict[str, str]: ユーザー認証結果

        Raises:
            ApiException: メールアドレス または パスワードが未入力の場合
        """
        credentials = {
            'username': schema.username,
            'password': schema.password,
        }

        # メールアドレスとパスワードが入力されている場合、
        # ユーザー認証を実施してアクセストークンとリフレッシュトークンを生成
        if all(credentials.values()):
            user = cls().__authenticate(request, **credentials)
            # アクセストークンのクレームセット取得
            access_token_claims = jwt_claims_handler(
                user,
                token_type=TYPE_ACCESS_TOKEN)

        # メールアドレス または パスワードが未入力の場合はエラー
        else:
            raise ApiException(create_error(ErrorMessage.INVALID_EMAIL_OR_PASSWORD))

        # アクセストークンを返す
        return jwt_response_handler(jwt_encode_handler(access_token_claims))

    def __authenticate(
        self,
        request: Request,
        username: str = None,
        password: str = None
    ) -> User:
        """ ユーザー認証

        Args:
            request (Request): リクエスト情報
            username (str): ユーザー名
            password (str): パスワード

        Returns:
            User: ユーザー情報

        Raises:
            ApiException:
                ・入力されたメールアドレスでユーザーを取得できなかった場合
                ・入力されたパスワードとユーザーのパスワードが一致しなかった場合
                ・入力されたメールアドレスで取得したユーザーが有効でない場合
        """
        user = CRUDUser(request.state.db_session).get_query().filter_by(**{'username': username}).all()

        # ユーザーを取得できなかった場合はエラー
        if not user:
            raise ApiException(create_error(ErrorMessage.FAILURE_LOGIN))

        # パスワードが一致しない もしくは ユーザーが有効でない場合はエラー
        if not check_password(password, user[0].password) or not user[0].is_active:
            raise ApiException(create_error(ErrorMessage.FAILURE_LOGIN))

        return user[0]
