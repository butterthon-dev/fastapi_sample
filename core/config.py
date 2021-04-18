import os
from functools import lru_cache
from pydantic import BaseSettings

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Environment(BaseSettings):
    """ 環境変数を読み込むファイル
    """
    allow_headers: list
    allow_origins: list
    debug: bool
    database_url: str
    test_database_url: str
    jwt_algorithm: str
    jwt_secret_key: str
    jwt_access_token_expire: int
    jwt_refresh_token_expire: int

    class Config:
        env_file = os.path.join(PROJECT_ROOT, '.env')


@lru_cache
def get_env():
    return Environment()
