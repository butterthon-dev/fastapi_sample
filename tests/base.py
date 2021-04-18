from fastapi.testclient import TestClient

from tests.conftest import test_app
from tests.db_session import get_test_db_session, set_current_test_db_session


class BaseTestCase:
    """ ベーステストクラス

    Attributes:
        client (FastAPI): APIクライアント
    """
    client = TestClient(test_app)

    def setup_method(self, method) -> None:
        """ テストケースごとの前処理
        """
        self.db_session = get_test_db_session()
        set_current_test_db_session(self.db_session)

    def teardown_method(self, method) -> None:
        """ 後処理
        """
        self.db_session.test_db_session_remove()  # ロールバック
