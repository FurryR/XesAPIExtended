from typing import TypedDict, TypeVar, Optional
from http.cookies import SimpleCookie
from .base import APIException
import aiohttp


class Info_Data(TypedDict):
    """
    学而思回传的 InfoData。
    """

    auth: str  # 未知
    avatar_default: int  # 未知
    avatar_path: str  # 头像链接
    avatar_version: str  # 头像上传日期（Unix 时间戳）
    bussinessline_id: int  # 未知
    create_time: str  # 账户创建时间
    email: str  # email
    en_name: str  # 英文名
    encrypt_user_id: str  # 未知
    grade_alias: str  # 别名，参照 grade_id 和 grade_name
    grade_id: int  # 学历
    grade_name: str  # 人类可读学历
    id: str  # 学员 ID
    name: str  # 同 id
    nickname: str  # 昵称
    realname: str  # 真名
    role: str  # 未知
    sex: str  # 性别(参照 API 返回结果)
    status: str  # 未知
    tal_cg_id: int  # 未知
    tal_id: str  # 好未来 ID
    uid: str  # 账户的 UID（不是学员 ID）
    user_id: str  # 同 id
    xes_encrypt_uid: str  # 加密了的 UID


T = TypeVar("T")


class APIResponse(TypedDict):
    stat: int
    status: int
    msg: str
    data: Optional[T]


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
                if c["stat"] != 1:
                    raise APIException(c["msg"])
                return c["data"]
