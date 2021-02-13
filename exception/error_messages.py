class BaseMessage:
    """ メッセージクラスのベース
    """
    text: str

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessage:
    """ メッセージクラス
    """
    class INTERNAL_SERVER_ERROR(BaseMessage):
        text = 'システムエラーが発生しました、管理者に問い合わせてください'

    class FAILURE_LOGIN(BaseMessage):
        text = 'ログイン失敗'
