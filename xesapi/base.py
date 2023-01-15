class APIException(Exception):
    """
    API 错误信息。
    """

    what: str  # 错误信息

    def __init__(self, what: str):
        """
        构造 API 错误实例。

        Args:
            what (str): 错误消息。
        """
        self.what = what

    def __str__(self) -> str:
        return f"<APIException what={repr(self.what)}>"
