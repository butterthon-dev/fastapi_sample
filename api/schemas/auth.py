# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
authのスキーマ定義
"""

from fastapi.param_functions import Form

from core.config import get_env
from migrations.models import User

MAX_LENGTH_USERNAME = User.username.property.columns[0].type.length
MAX_LENGTH_PASSWORD = User.password.property.columns[0].type.length


class AuthRequestSchema:
    """ 認証に関するスキーマ
    """
    def __init__(
        self,
        username: str = Form(..., max_length=MAX_LENGTH_USERNAME),
        password: str = Form(..., max_length=MAX_LENGTH_PASSWORD)
    ):
        """ 初期処理

        Args:
            username (str):
                ・ユーザー名
                ・必須パラメータ

            password (str):
                ・パスワード
                ・必須パラメータ
        """
        self.username = username
        self.password = password
