from typing import Optional

from fastapi import security, Request, status
from starlette import authentication

from exceptions import ApiException, create_error
from exceptions.error_messages import ErrorMessage
from migrations.models import User


class OAuth2PasswordBearer(security.OAuth2PasswordBearer):
    """ OAuth2PasswordBearerのラッパー
    """
    async def __call__(self, request: Request) -> Optional[str]:
        """ 呼び出し可能インスタンス
        Args:
            request (Request): リクエスト情報

        Returns:
            Optional[str]: JsonWebToken

        Raises:
            ApiException: ヘッダーに認証情報（Authorization）が含まれていない場合
        """
        authorization: str = request.headers.get('Authorization')
        scheme, param = security.utils.get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != 'bearer':
            if self.auto_error:
                raise ApiException(create_error(ErrorMessage.INVALID_TOKEN), status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                return None
        return param


class AuthenticatedUser(authentication.SimpleUser):
    """ 承認済みユーザー
    """
    def __init__(self, user: User) -> None:
        self.id = user.id
        self.username = user.username


class UnauthenticatedUser(authentication.UnauthenticatedUser):
    """ 未承認ユーザー
    """
    pass
