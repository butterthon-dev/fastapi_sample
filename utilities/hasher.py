# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
このモジュールはパスワードハッシュに関するユーティリティ提供する
"""
import base64
import hashlib
import hmac
from typing import Any

from utilities.string import StringUtils


class PasswordHasher:
    """ PBKDF2アルゴリズムを使用したパスワードハッシュクラス

    PBKDF2, HMAC, SHA256で構成する

    Attributes:
        algorithm (str): 暗号化アルゴリズム
        digest (_Hash): Hashクラス
    """
    algorithm = 'pbkdf2_sha256'
    digest = hashlib.sha256

    def encode(
        self,
        plain_password: str,
        salt: str,
        iterations: int = 36000
    ) -> str:
        """ 平文のパスワードをハッシュ化する

        Args:
            plain_password (str): 平文のパスワード
            salt (str): ソルト値
            iterations (str): ストレッチングの回数

        Returns:
            str: 平文のパスワードをハッシュ化した文字列

        Raises:
            AssertionError:
                ・平文のパスワードが空文字やNoneが指定された場合
                ・ソルト値に空文字やNoneが指定された、またはソルト値に"$"が含まれてしまっている場合
        """
        assert plain_password is not None
        assert salt and '$' not in salt

        # 平文のパスワード と ソルト値を結合してiterationsの回数分ストレッチング
        hash = self.__pbkdf2(
            plain_password,
            salt,
            iterations,
            self.digest
        )
        hash = base64.b64encode(hash).decode('ascii').strip()

        # 「アルゴリズム名」「ストレッチング回数」「ソルト値」「ハッシュ値」を結合した文字列を返す
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """ 平文のパスワードとハッシュ化されたパスワードを検証する

        Args:
            plain_password (str): 平文のパスワード
            hashed_password (str): ハッシュ化されたパスワード

        Returns:
            bool: 平文のパスワードとハッシュ化されたパスワードのハッシュ値が一致する場合はTrue、一致しない場合はFalse
        """
        _, iterations, salt, _ = hashed_password.split('$', 3)
        encoded_2 = self.encode(plain_password, salt, int(iterations))
        return self.__constant_time_compare(hashed_password, encoded_2)

    def __pbkdf2(
        self,
        plain_password: str,
        salt: str,
        iterations: int,
        digest: Any,
        dklen: int = 0,
    ) -> str:
        """ PBKDF2アルゴリズムを使用して平文のパスワードをハッシュ化して返す

        Args:
            plain_password (str): 平文のパスワード
            salt (str): ソルト値
            iterations (int): ストレッチングの回数
            digest (Any): ハッシュ関数
            dklen (int): 生成鍵長(オクテット)

        Returns:
            str: パスワードをハッシュ化した文字列
        """
        dklen = dklen or None
        plain_password = self.__force_bytes(plain_password)
        salt = self.__force_bytes(salt)
        return hashlib.pbkdf2_hmac(
            digest().name, plain_password, salt, iterations, dklen
        )

    def __constant_time_compare(self, value1: str, value2: str) -> bool:
        """ 2つの文字列（value1 と value2）が等しいかどうか

        Args:
            value1 (str): 文字列1
            value2 (str): 文字列2

        Returns:
            bool: 文字列が等しい場合はTrue, 等しくない場合はFalse
        """
        return hmac.compare_digest(
            self.__force_bytes(value1),
            self.__force_bytes(value2)
        )

    def __force_bytes(
        self,
        s,
        encoding: str = 'utf-8',
        errors: str = 'strict',
    ) -> bytes:
        """ 引数encodingで指定されたエンコーディングルール通りに変換したバイトデータを返す

        Args:
            s: エンコーディングしたい文字列
            errors (str): エンコーディングルールに従った変換ができなかった場合の対応方法、デフォルトは'strict'（UnicodeDecodeErrorをスローする）

        Returns:
            bytes:  エンコーディングされたバイトデータ
        """
        # 引数sがバイトデータの場合
        if isinstance(s, bytes):
            # 引数encodingがutf-8の場合、sをそのまま返す
            if encoding == 'utf-8':
                return s

            # 上記以外は、引数sを指定のエンコーディングルール通りに変換したバイトデータを返す
            else:
                return s.decode('utf-8', errors).encode(encoding, errors)
        return str(s).encode(encoding, errors)


def is_hashed_password_usable(hashed_password: str) -> bool:
    """ ハッシュ化されたパスワードが正当な値かどうか

    Args:
        hashed_password (str): ハッシュ化されたパスワード

    Returns:
        bool: 正当な値であればTrue、それ以外はFalse
    """
    return hashed_password is None or not hashed_password.startswith('!')


def check_password(plain_password: str, hashed_password: str) -> bool:
    """ 平文パスワードがハッシュ化されたパスワードと一致するかどうか

    Args:
        plain_password (str): 平文パスワード
        hashed_password (str): ハッシュ化されたパスワード

    Returns:
        bool: 平文のパスワードとハッシュ化されたパスワードのハッシュ値が一致する場合はTrue、一致しない場合はFalse
    """
    if plain_password is None\
            or not is_hashed_password_usable(hashed_password):
        return False
    return PasswordHasher().verify(plain_password, hashed_password)


def make_password(plain_password: str) -> str:
    """ パスワードをハッシュ化して返す

    Args:
        plain_password (str): 平文パスワード

    Returns:
        str: パスワードをハッシュ化した文字列
    """
    return PasswordHasher().encode(plain_password, StringUtils.get_random_string())
