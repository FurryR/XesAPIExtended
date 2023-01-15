from typing import TypedDict, TypeVar, Optional
from .base import APIException
from .user import User
import aiohttp

class TalToken_Data(TypedDict):
    """
    TalToken 的内部 data。
    """

    code: str  # 唯一标识符，可以在 https://login.xueersi.com/V1/Web/getToken 使用。
    passport_token: str  # 好未来 token，用于 Cookie（tal_id）。


class Captcha_Data(TypedDict):
    """
    Captcha 的内部 data。
    """

    captcha: str  # base64 url, data:image\\/jpeg;base64,...


T = TypeVar("T")


class LoginResponse(TypedDict):
    """
    API 接口返回内容的类型注解。
    """

    errcode: int  # 错误码
    errmsg: str  # 错误消息
    data: Optional[T]  # 数据


class Captcha:
    """
    验证码 API。
    """

    __username: str
    __password: str
    __image: str

    def __init__(self, username: str, password: str, image: str):
        """
        生成 Captcha 实例。

        Args:
            username (str): 用户名。
            password (str): 密码。
            image (str): Captcha base64 url。
        """
        self.__username, self.__password, self.__image = username, password, image

    @property
    def image(self) -> str:
        """
        获得 base64 image url。

        Returns:
            str: _base64 image url
        """
        return self.__image

    async def resolve(self, captcha: str) -> User:
        """
        完成Captcha。

        Args:
            captcha (str): captcha 对应的输入

        Raises:
            LoginException: 登录失败的情况

        Returns:
            User: 用户实例
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://passport.100tal.com/v1/web/login/pwd",
                data={
                    "symbol": self.__username,
                    "password": self.__password,
                    "captcha": captcha,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "client-id": "111101",
                    "device-id": "_",
                    "ver-num": "0.0.0",
                    "referer": "https://login.xueersi.com/",
                },
            ) as req:
                c: LoginResponse[TalToken_Data] = await req.json()
                if c["errcode"] != 0 or c["data"] == None:
                    raise APIException(c["errmsg"])
                async with session.post(
                    "https://login.xueersi.com/V1/Web/getToken",
                    data={"code": c["data"]["code"]},
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "client-id": "111101",
                        "device-id": "_",
                        "ver-num": "0.0.0",
                        "referer": "https://login.xueersi.com/",
                    },
                ) as req2:
                    return User(req2.cookies)


async def login(username: str, password: str) -> Captcha:
    """
    进行登录操作。

    Args:
        username (str): 用户名（手机号，邮箱等）
        password (str): 密码

    Raises:
        APIException: API 错误

    Returns:
        Captcha: 验证码实例。
    """
    async with aiohttp.ClientSession("https://passport.100tal.com/") as session:
        async with session.post(
            "/v1/web/captcha/get",
            data={
                "symbol": username,
                "password": password,
                "scene": 3,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "client-id": "111101",
                "device-id": "_",
                "ver-num": "0.0.0",
                "referer": "https://login.xueersi.com/",
            },
        ) as req:
            c: LoginResponse[Captcha_Data] = await req.json()
            if c["errcode"] != 0:
                raise APIException(c["errmsg"])
            return Captcha(username, password, c["data"]["captcha"])
