from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from tests.db_session import get_current_test_db_session


class TestDBSessionMiddleware(BaseHTTPMiddleware):
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
        request.state.db_session = get_current_test_db_session()
        return await call_next(request)
