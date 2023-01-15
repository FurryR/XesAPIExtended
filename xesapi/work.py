import aiohttp
from .user import User, APIResponse
from .type import Work_Data, Comment_Data, ReplyList_Data, Reply_Data, GetComment_Data
from .base import APIException
from typing import Optional, AsyncGenerator, Any


class Reply:
    __data: Reply_Data
    __user: Optional[User]

    async def send(self, content: str):
        """
        回复这个评论。

        Args:
            content (str): 内容

        Raises:
            APIException: API 错误
        """
        if self.__user == None:
            raise APIException("未登录")
        else:
            async with aiohttp.ClientSession(
                "https://code.xueersi.com/", cookies={"xes_rfh": self.__user.xes_rfh}
            ) as session:
                async with session.post(
                    "/api/comments/submit",
                    data={
                        "appid": 1001108,
                        "content": content,
                        "target_id": self.__data["id"],
                        "topic_id": self.__data["topic_id"],
                    },
                    headers={"Content-Type": "application/json", "User-Agent": "_"},
                ) as req:
                    c: APIResponse[None] = await req.json()
                    if c["stat"] != 1:
                        raise APIException(
                            c["message"] if c["msg"] == None else c["msg"]
                        )

    def __init__(self, data: Reply_Data, user: Optional[User] = None):
        """
        实例化一个回复。

        Args:
            data (Reply_Data): 回复数据。
            user (Optional[User], optional): 用户上下文。默认为 None。
        """
        self.__data, self.__user = data, user


class Comment:
    __data: Comment_Data
    __user: Optional[User]

    async def send(self, content: str):
        """
        在这个评论下发布回复。

        Args:
            content (str): 内容

        Raises:
            APIException: API 错误
        """
        if self.__user == None:
            raise APIException("未登录")
        else:
            async with aiohttp.ClientSession(
                "https://code.xueersi.com/", cookies={"xes_rfh": self.__user.xes_rfh}
            ) as session:
                async with session.post(
                    "/api/comments/submit",
                    data={
                        "appid": 1001108,
                        "content": content,
                        "target_id": self.__data["id"],
                        "topic_id": self.__data["topic_id"],
                    },
                    headers={"Content-Type": "application/json", "User-Agent": "_"},
                ) as req:
                    c: APIResponse[None] = await req.json()
                    if c["stat"] != 1:
                        raise APIException(
                            c["message"] if c["msg"] == None else c["msg"]
                        )

    async def reply(self) -> AsyncGenerator[Reply, Any]:
        """
        获得评论。

        Returns:
            AsyncGenerator[Comment]: 评论生成器，使用async for遍历
        """
        if not self.__data["reply_list"]["hasMore"]:
            for i in self.__data["reply_list"]["data"]:
                yield Reply(i, self.__user)
        else:
            async with aiohttp.ClientSession(
                "https://code.xueersi.com/",
                cookies={} if self.__user == None else {"xes_rfh": self.__user.xes_rfh},
            ) as session:
                page = 1
                while True:
                    async with session.get(
                        "/api/comments?appid=1001108&topic_id="
                        + self.__data["topic_id"]
                        + "&parent_id="
                        + self.__data["id"]
                        + f"&order_type=time&page={page}&per_page=10",
                        headers={"User-Agent": "_"},
                    ) as req:
                        c: APIResponse[GetComment_Data[Reply_Data]] = await req.json()
                        if c["stat"] != 1 or c["data"] == None:
                            raise APIException(
                                c["message"] if c["msg"] == None else c["msg"]
                            )
                        for i in c["data"]["data"]:
                            yield Reply(i, self.__user)
                        if len(c["data"]["data"]) != 10:
                            break
                        else:
                            page += 1

    def __init__(self, data: Comment_Data, user: Optional[User] = None):
        """
        实例化一个评论。

        Args:
            data (Comment_Data): 评论数据。
            user (Optional[User], optional): 用户上下文。默认为 None。
        """
        self.__data, self.__user = data, user


class Work:
    __data: Work_Data
    __user: Optional[User]

    async def like(self):
        """
        喜欢这个作品。

        Raises:
            APIException: API 错误
        """
        if self.__user == None:
            raise APIException("未登录")
        else:
            async with aiohttp.ClientSession(
                "https://code.xueersi.com/", cookies={"xes_rfh": self.__user.xes_rfh}
            ) as session:
                async with session.post(
                    "/api/compilers/40576653/like",
                    data={
                        "params": {
                            "id": str(self.__data["id"]),
                            "lang": "code",
                            "form": self.__data["lang"],
                        }
                    },
                    headers={"User-Agent": "_"},
                ) as req:
                    c: APIResponse[None] = await req.json()
                    if c["stat"] != 1:
                        raise APIException(
                            c["message"] if c["msg"] == None else c["msg"]
                        )
                    self.__data["likes"] += 1

    async def unlike(self):
        """
        踩这个作品。

        Raises:
            APIException: API 错误
        """
        if self.__user == None:
            raise APIException("未登录")
        else:
            async with aiohttp.ClientSession(
                "https://code.xueersi.com/", cookies={"xes_rfh": self.__user.xes_rfh}
            ) as session:
                async with session.post(
                    "/api/compilers/40576653/unlike",
                    data={
                        "params": {
                            "id": str(self.__data["id"]),
                            "lang": "code",
                            "form": self.__data["lang"],
                        }
                    },
                    headers={"User-Agent": "_"},
                ) as req:
                    c: APIResponse[None] = await req.json()
                    if c["stat"] != 1:
                        raise APIException(
                            c["message"] if c["msg"] == None else c["msg"]
                        )
                    self.__data["likes"] += 1

    async def send(self, content: str):
        """
        在这个作品下发布评论。

        Args:
            content (str): 内容

        Raises:
            APIException: API 错误
        """
        if self.__user == None:
            raise APIException("未登录")
        else:
            async with aiohttp.ClientSession(
                "https://code.xueersi.com/", cookies={"xes_rfh": self.__user.xes_rfh}
            ) as session:
                async with session.post(
                    "/api/comments/submit",
                    data={
                        "appid": 1001108,
                        "content": content,
                        "target_id": 0,
                        "topic_id": self.__data["topic_id"],
                    },
                    headers={"Content-Type": "application/json", "User-Agent": "_"},
                ) as req:
                    c: APIResponse[None] = await req.json()
                    if c["stat"] != 1:
                        raise APIException(
                            c["message"] if c["msg"] == None else c["msg"]
                        )

    async def comment(self) -> AsyncGenerator[Comment, Any]:
        """
        获得评论。

        Returns:
            AsyncGenerator[Comment]: 评论生成器，使用async for遍历
        """
        async with aiohttp.ClientSession(
            "https://code.xueersi.com/",
            cookies={} if self.__user == None else {"xes_rfh": self.__user.xes_rfh},
        ) as session:
            page = 1
            while True:
                async with session.get(
                    "/api/comments?appid=1001108&topic_id="
                    + self.__data["topic_id"]
                    + f"&parent_id=0&order_type=time&page={page}&per_page=15",
                    headers={"User-Agent": "_"},
                ) as req:
                    c: APIResponse[GetComment_Data[Comment_Data]] = await req.json()
                    if c["stat"] != 1 or c["data"] == None:
                        raise APIException(
                            c["message"] if c["msg"] == None else c["msg"]
                        )
                    for i in c["data"]["data"]:
                        yield Comment(i, self.__user)
                    if len(c["data"]["data"]) != 15:
                        break
                    else:
                        page += 1

    def __init__(self, data: Work_Data, user: Optional[User] = None):
        """
        实例化一个作品。

        Args:
            data (Work_Data): 作品数据。
            user (Optional[User], optional): 用户上下文。默认为 None。
        """
        self.__data, self.__user = data, user


async def get_work(id: int, user: Optional[User] = None) -> Work:
    """
    获得作品。

    Args:
        id (int): 作品id。
        user (Optional[User], optional): 用户上下文。默认为 None。

    Raises:
        APIException: API 错误

    Returns:
        Work: 作品实例
    """
    async with aiohttp.ClientSession(
        "https://code.xueersi.com/",
        cookies={} if user == None else {"xes_rfh": user.xes_rfh},
    ) as session:
        async with session.get(f"/api/compilers/v2/{id}") as req:
            c: APIResponse[Work_Data] = await req.json()
            if c["stat"] != 1 or c["data"] == None:
                raise APIException(c["message"] if c["msg"] == None else c["msg"])
            return Work(c["data"], user)
