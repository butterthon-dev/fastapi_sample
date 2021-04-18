from threading import local as thread_local

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from core.config import get_env

_thread_local = thread_local()


def set_current_test_db_session(db_session: scoped_session) -> None:
    """ スレッドローカルにテスト用のDBセッションをセット

    Args:
        db_session (scoped_session): テスト用のDBセッション
    """
    setattr(_thread_local, 'db_session', db_session)


def get_current_test_db_session() -> scoped_session:
    """ スレッドローカルからテスト用のDBセッションを取得

    Returns:
        scoped_session: テスト用のDBセッション
    """
    return getattr(_thread_local, 'db_session')


class TestingDBSession(Session):
    """ commit()の挙動を変えるため、Sessionクラスをオーバーライド
    """
    def commit(self):
        # データアクセスクラス（fastapi_sample/crud）やAPIの中でflush()は実行する想定なので、
        # ここでflush()はとりあえず不要
        # self.flush()
        self.expire_all()


class test_scoped_session(scoped_session):
    """ リクエストミドルウェアのremove()で何も実行されないように、scoped_sessionクラスをオーバーライド
    """
    def remove(self):
        pass

    def test_db_session_remove(self):
        """ テストDB用のremove()
        """
        if self.registry.has():
            self.registry().close()
        self.registry.clear()


test_db_connection = create_engine(
    get_env().test_database_url,
    encoding='utf8',
    pool_pre_ping=True,
)


def get_test_db_session():
    """ テストDBセッションを返す
    """
    return test_scoped_session(
        sessionmaker(
            bind=test_db_connection,
            class_=TestingDBSession,
            expire_on_commit=False,
        )
    )
