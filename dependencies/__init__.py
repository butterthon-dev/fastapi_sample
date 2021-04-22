from fastapi import Depends, Request, status

from exceptions import ApiException, create_error
from exceptions.error_messages import ErrorMessage
from utilities.authentication import OAuth2PasswordBearer

OAUTH2_SCHEMA = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


async def login_required(
    request: Request,
    token: str = Depends(OAUTH2_SCHEMA)
) -> None:
    """ ユーザがログインしているかどうか

    Args:
        request (Request): リクエスト情報
        token (str): アクセストークン

    Raises:
        ApiException: ログインに失敗している場合
    """
    if not request.user.is_authenticated:
        raise ApiException((create_error(ErrorMessage.INVALID_TOKEN)), status_code=status.HTTP_401_UNAUTHORIZED)
