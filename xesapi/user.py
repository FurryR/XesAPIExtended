from typing import TypedDict, TypeVar, Optional, Union, TypeAlias
from http.cookies import SimpleCookie
from .base import APIException
from .type import Info_Data
import aiohttp

T = TypeVar("T")


class _APIResponse(TypedDict):
    stat: int
    status: int
    msg: str
    data: Optional[T]


class _FailedAPIResponse(TypedDict):
    status_code: int
    message: str


APIResponse: TypeAlias = Union[_APIResponse, _FailedAPIResponse]


class User:
    __cookie: SimpleCookie

    def __init__(self, cookie: SimpleCookie):
        """
        初始化 User 类。

        Args:
            cookie (SimpleCookie): cookie
        """
        self.__cookie = cookie

    @property
    def tal_token(self) -> Optional[str]:
        """
        获得好未来 token。不建议使用此接口。

        Returns:
            Optional[str]: 好未来 token
        """
        return self.__cookie["tal_token"].value

    @property
    def xes_rfh(self) -> Optional[str]:
        """
        获得 xes_rfh。不建议使用此接口。

        Returns:
            Optional[str]: xes_rfh
        """
        return self.__cookie["xes_rfh"].value

    async def info(self) -> Optional[Info_Data]:
        """
        获得个人信息。

        Raises:
            APIException: API 错误。

        Returns:
            Optional[Info_Data]: 个人信息。当未登录时，返回 None。
        """
        async with aiohttp.ClientSession(
            "https://code.xueersi.com/", cookies={"xes_rfh": self.xes_rfh}
        ) as session:
            async with session.get("/api/user/info") as req:
                c: APIResponse[Info_Data] = await req.json()
                if c["stat"] != 1 or c["data"] == None:
                    raise APIException(c["message"] if c["msg"] == None else c["msg"])
                return c["data"]
