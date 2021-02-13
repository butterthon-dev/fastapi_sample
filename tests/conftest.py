import psycopg2
from core.config import get_env
from migrations.models import Base
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, drop_database
from tests.db_session import test_db_connection

# conftestで初期データを登録する場合はこのSessionを使用する
# Session = scoped_session(
#     sessionmaker(
#         bind=test_db_connection
#     )
# )


def create_test_database():
    # テストDBが削除されずに残ってしまっている場合は削除
    if database_exists(get_env().test_database_url):
        drop_database(get_env().test_database_url)

    # テストDB作成
    _con = \
        psycopg2.connect('host=db user=postgres password=postgres')
    _con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    _cursor = _con.cursor()
    _cursor.execute('CREATE DATABASE test_db_fastapi_sample')

    # テストDBにテーブル追加
    Base.metadata.create_all(bind=test_db_connection)


def pytest_sessionstart(session):
    """ pytest実行時に一度だけ呼ばれる処理
    """
    # テストDB作成
    create_test_database()


def pytest_sessionfinish(session, exitstatus):
    """ pytest終了時に一度だけ呼ばれる処理
    """
    # テストDB削除
    if database_exists(get_env().test_database_url):
        drop_database(get_env().test_database_url)
