from crud.base import get_db_session
from fastapi.testclient import TestClient
from main import app
from tests.db_session import get_test_db_session


class BaseTestCase:
    def setup_method(self, method):
        """ 前処理
        """
        self.db_session = get_test_db_session()

        # APIクライアントの設定
        self.client = TestClient(app, base_url='https://localhost',)

        # DBをテスト用のDBでオーバーライド
        app.dependency_overrides[get_db_session] = \
            self.override_get_db

    def teardown_method(self, method):
        """ 後処理
        """
        self.db_session.test_db_session_remove()  # ロールバック

        # オーバーライドしたDBを元に戻す
        app.dependency_overrides[self.override_get_db] = \
            get_db_session

    def override_get_db(self):
        """ DBセッションの依存性オーバーライド関数
        """
        yield self.db_session
