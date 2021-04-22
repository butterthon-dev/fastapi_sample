# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
このモジュールは文字列操作に関するユーティリティを提供する
"""
import random


class StringUtils:
    """ 文字列に関するユーティリティ
    """
    @classmethod
    def get_random_string(
        cls,
        length: int = 12,
        allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        digit=True,
        symbol=False,
    ) -> str:
        """ ランダムな文字列を生成する

        Args:
            length (int): 生成する文字列の長さ
            allowed_chars (str): 使用する文字
            digit (bool): 数字を含めるかどうか
            symbol (bool): 記号を含めるかどうか

        Returns:
            str: 指定の長さのランダムな文字列
        """
        if digit:
            allowed_chars += '1234567890'
        if symbol:
            allowed_chars += '-._~'  # 記号はURIで使用できる記号のみ
        return ''.join(random.choice(allowed_chars) for i in range(length))
