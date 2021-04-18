from fastapi import Depends, Request
from crud import get_db_session
from sqlalchemy.orm import scoped_session


async def set_db_session_in_request(
    request: Request,
    db_session: scoped_session = Depends(get_db_session)
):
    """ リクエストにDBセッションをセットする
    """
    request.state.db_session = db_session
