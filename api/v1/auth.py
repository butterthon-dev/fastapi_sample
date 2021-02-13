from fastapi import Request


class AuthAPI:
    """ 認証に関するAPI
    """
    @classmethod
    def login(cls, request: Request):
        """ ログインAPI
        """
        return 'ログイン成功'
