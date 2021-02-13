from crud.base import BaseCRUD
from migrations.models import User


class CRUDUser(BaseCRUD):
    """ ユーザーデータアクセスクラスのベース
    """
    model = User
