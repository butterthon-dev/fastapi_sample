from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.security.utils import get_authorization_scheme_param  # 追加
from jose import jwt  # 追加
from starlette.middleware import authentication, cors  # authentication追加
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from core.config import get_env
from crud import get_db_session
from crud.crud_user import CRUDUser  # 追加
from exceptions import (
    ApiException,
    create_error,
    SystemException,
)
from exceptions.error_messages import ErrorMessage  # 追加
from utilities.authentication import AuthenticatedUser, UnauthenticatedUser  # 追加
from utilities.jwt_handler import jwt_decord_handler  # 追加


class CORSMiddleware(cors.CORSMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            allow_origins=get_env().allow_origins,
            allow_methods=cors.ALL_METHODS,
            allow_headers=get_env().allow_headers,
            allow_credentials=True,
        )


class DBSessionMiddleware(BaseHTTPMiddleware):
    """ リクエスト情報にDBセッションを設定するミドルウェア
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        """ ミドルウェアの処理

        Args:
            request (Request): リクエスト情報
            call_next (method): 次の処理

        Returns:
            Response: レスポンス
        """
        request.state.db_session = get_db_session()
        return await call_next(request)


class HttpRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)

        except ApiException as ae:
            request.state.db_session.rollback()
            return JSONResponse(
                ae.detail,
                status_code=ae.status_code)

        # 予期せぬ例外
        except Exception as e:
            request.state.db_session.rollback()
            se = SystemException(e)
            print(se.stack_trace)
            return JSONResponse(
                se.detail,
                status_code=se.status_code)

        # 正常終了時
        else:
            request.state.db_session.commit()
            return response

        # DBセッションの破棄は必ず行う
        finally:
            request.state.db_session.remove()


class AuthenticationBackend(authentication.AuthenticationBackend):
    """ 認証ミドルウェアのバックエンド

    このミドルウェアを認証バックエンドとして使用することで、リクエストのユーザー情報に「request.user」でアクセス可能になる
    """
    async def authenticate(self, request: Request) -> None:
        """ 認証処理

        Args:
            request (Request): リクエスト情報
        """
        authorization: str = request.headers.get('Authorization')
        scheme, access_token = get_authorization_scheme_param(authorization)

        # リクエストヘッダに認証情報が無い場合は「未承認ユーザー」を返す
        if not authorization or scheme.lower() != 'bearer':
            return authentication.AuthCredentials(['unauthenticated']), UnauthenticatedUser()

        # JWTをデコードしてクレームセットを取得
        try:
            claims = jwt_decord_handler(access_token)

        # アクセストークン期限切れ
        except jwt.ExpiredSignatureError:
            raise ApiException(create_error(ErrorMessage.EXPIRED_TOKEN), status_code=status.HTTP_401_UNAUTHORIZED)

        # その他エラーの場合は「未承認ユーザー」を返す
        except Exception as e:
            print(e)
            return authentication.AuthCredentials(['unauthenticated']), UnauthenticatedUser()

        # クレームセットのユーザーIDでユーザーを取得
        user = CRUDUser(request.state.db_session).get_by_id(claims['user_id'])

        # 下記いずれかの場合はエラー
        # ・ユーザーを取得できなかった場合
        # ・ユーザーを取得できたが、非アクティブ
        if not user or not user.is_active:
            raise ApiException(create_error(ErrorMessage.INVALID_TOKEN))
        return authentication.AuthCredentials(['authenticated']), AuthenticatedUser(user)
