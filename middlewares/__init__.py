from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware import cors
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from core.config import get_env
from crud import get_db_session
from exceptions import (
    ApiException,
    SystemException,
)


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
