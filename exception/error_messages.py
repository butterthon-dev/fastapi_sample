import os
from configparser import ConfigParser
from core.config import PROJECT_ROOT
from functools import lru_cache

MESSAGES_INI = ConfigParser()
MESSAGES_INI.read(
    os.path.join(PROJECT_ROOT, 'core/error_messages.ini'),
    'utf-8'
)


@lru_cache
def get(key: str, *args):
    return MESSAGES_INI.get('messages', key).format(*args)


INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
FAILURE_LOGIN = 'FAILURE_LOGIN'
