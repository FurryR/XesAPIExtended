# local imports
import sys
sys.path.append("..")

from xesapi import login, Captcha, User, Info_Data
from typing import Union, Callable, Optional
from customtkinter import CTkFont
from PIL import Image, ImageTk
from tkinter import Event
import customtkinter as ctk
import asyncio
import base64
import io


def base64_url_processor(url: str) -> bytes:
    """
    将 base64 url image 转换为 bytes。

    Args:
        url (str): base64 url 图像

    Returns:
        bytes: 字节对象
    """
    if url.startswith("data:image/jpeg;base64,"):
        return base64.b64decode(url[23:])
    else:
        raise Exception()


class LoginScene:
    """
    登录 Scene，显示登录框。
    """

    title: ctk.CTkLabel
    username_label: ctk.CTkLabel
    username_entry: ctk.CTkEntry
    password_label: ctk.CTkLabel
    password_entry: ctk.CTkEntry
    login_button: ctk.CTkButton
    callback: Callable[[str, str], None]

    def __do_callback(self):
        self.callback(self.username_entry.get(), self.password_entry.get())

    def __username_entry_enter(self, _: Event):
        if self.password_entry.get() != "":
            self.__do_callback()
        else:
            self.password_entry.focus()

    def __password_entry_enter(self, _: Event):
        self.__do_callback()

    def destroy(self):
        """
        销毁 LoginScene。
        """
        self.title.destroy()
        self.username_label.destroy()
        self.username_entry.destroy()
        self.password_label.destroy()
        self.password_entry.destroy()
        self.login_button.destroy()

    def __init__(self, root: ctk.CTk, callback: Callable[[str, str], None]):
        """
        初始化 LoadingScene。

        Args:
            root (ctk.CTk): Tkinter 根
            callback (callable[[str, str], None]): 登录回调事件
        """
        self.callback = callback
        self.title = ctk.CTkLabel(
            root, text="[1/3] 登录到学而思", font=CTkFont("Microsoft YaHei", 20, 'bold')
        )
        self.username_label = ctk.CTkLabel(root, text="账户:")
        self.username_entry = ctk.CTkEntry(root)
        self.password_label = ctk.CTkLabel(root, text="密码:")
        self.password_entry = ctk.CTkEntry(root, show="*")
        self.login_button = ctk.CTkButton(root, text="登录")
        self.title.place(x=0, y=0)
        self.username_label.place(x=50, y=30)
        self.username_entry.place(x=100, y=30)
        self.password_label.place(x=50, y=70)
        self.password_entry.place(x=100, y=70)
        self.login_button.place(x=75, y=120)
        self.login_button.configure(command=self.__do_callback)
        self.username_entry.bind("<Return>", self.__username_entry_enter)
        self.password_entry.bind("<Return>", self.__password_entry_enter)


class CaptchaScene:
    """
    验证码 Scene，显示验证码。
    """

    title: ctk.CTkLabel
    image: ctk.CTkLabel
    tk_img: ImageTk.PhotoImage
    captcha_label: ctk.CTkLabel
    captcha_entry: ctk.CTkEntry
    callback: Callable[[str], None]

    def __captcha_entry_keypress(self, event: Event):
        v = self.captcha_entry.get()
        if (
            (event.keycode >= ord("a") and event.keycode <= ord("z"))
            or (event.keycode >= ord("A") and event.keycode <= ord("Z"))
            or (event.keycode >= ord("1") and event.keycode <= ord("9"))
        ) and len(v) == 3:
            self.callback(v + event.char)

    def __captcha_entry_validate(self, value: str):
        for item in value:
            i = ord(item)
            if (
                (i >= ord("a") and i <= ord("z"))
                or (i >= ord("A") and i <= ord("Z"))
                or (i >= ord("1") and i <= ord("9"))
            ):
                ...
            else:
                return False
        return True

    def destroy(self):
        """
        销毁 CaptchaScene。
        """
        self.title.destroy()
        self.image.destroy()
        self.captcha_label.destroy()
        self.captcha_entry.destroy()

    def __init__(self, root: ctk.CTk, image: bytes, callback: Callable[[str], None]):
        self.callback = callback
        self.title = ctk.CTkLabel(
            root, text="[2/3] 请通过机器人验证", font=CTkFont("Microsoft YaHei", 20, 'bold')
        )
        img = Image.open(io.BytesIO(image))
        self.tk_img = ctk.CTkImage(light_image = img, size=(img.width, img.height))
        self.image = ctk.CTkLabel(root, text="", image=self.tk_img)
        self.captcha_label = ctk.CTkLabel(root, text="验证码:")
        self.captcha_entry = ctk.CTkEntry(root)
        self.title.place(x=0, y=0)
        self.image.place(x=80, y=30)
        self.captcha_label.place(x=50, y=120)
        self.captcha_entry.place(x=100, y=120)
        self.captcha_entry.configure(
            validate="all",
            validatecommand=(root.register(self.__captcha_entry_validate), "%P"),
        )
        self.captcha_entry.bind("<KeyPress>", self.__captcha_entry_keypress)


class ResultScene:
    """
    结果 Scene，用于显示结果。
    """

    title: ctk.CTkLabel
    message: ctk.CTkLabel

    def destroy(self):
        """
        销毁 ResultScene。
        """
        self.title.destroy()
        self.message.destroy()

    def __init__(self, root: ctk.CTk):
        """
        初始化 LoadingScene。

        Args:
            root (ctk.CTk): Tkinter 根
        """
        self.title = ctk.CTkLabel(
            root, text="[3/3] 完成", font=CTkFont("Microsoft YaHei", 20, 'bold')
        )
        self.message = ctk.CTkLabel(root, text="请查看控制台输出获得结果。")
        self.title.place(x=0, y=0)
        self.message.place(x=0, y=30)


class LoadingScene:
    """
    加载时使用的 Scene。
    """

    title: ctk.CTkLabel

    def destroy(self):
        """
        销毁 LoadingScene。
        """
        self.message.destroy()

    def __init__(self, root: ctk.CTk):
        """
        初始化 LoadingScene。

        Args:
            root (ctk.CTk): Tkinter 根
        """
        self.message = ctk.CTkLabel(
            root, text="请稍等", font=CTkFont("Microsoft YaHei", 20, 'bold')
        )
        self.message.place(x=0, y=0)


class ErrorScene:
    """
    错误时使用的 Scene。
    """

    title: ctk.CTkLabel
    hint: ctk.CTkLabel
    temp: ctk.CTkLabel
    what: ctk.CTkLabel

    def destroy(self):
        """
        销毁 ErrorScene。
        """
        self.title.destroy()
        self.hint.destroy()
        self.temp.destroy()
        self.what.destroy()

    def __init__(self, root: ctk.CTk, message: str):
        """
        初始化 ErrorScene。

        Args:
            root (ctk.CTk): Tkinter 根
            message (str): 错误
        """
        self.title = ctk.CTkLabel(
            root, text="发生了一些错误", font=CTkFont("Microsoft YaHei", 20, 'bold')
        )
        self.hint = ctk.CTkLabel(root, text="请重启应用程序。")
        self.temp = ctk.CTkLabel(root, text="错误:")
        self.what = ctk.CTkLabel(root, text=f"{message}")
        self.what.configure(wraplength=root.winfo_width())
        self.title.place(x=0, y=0)
        self.hint.place(x=0, y=30)
        self.temp.place(x=0, y=80)
        self.what.place(x=0, y=110)


class App(ctk.CTk):
    captcha: Optional[Captcha]
    user: Optional[User]
    info: Optional[Info_Data]
    scene: Union[LoginScene, CaptchaScene, ResultScene, LoadingScene]
    eventloop: asyncio.AbstractEventLoop

    def __login(self, username: str, password: str):
        self.username, self.password = username, password
        self.scene.destroy()
        self.scene = LoadingScene(self)
        self.update()
        try:
            self.captcha = self.eventloop.run_until_complete(
                login(self.username, self.password)
            )
        except Exception as err:
            self.scene.destroy()
            self.scene = ErrorScene(self, str(err))
            return
        self.scene.destroy()
        self.scene = CaptchaScene(
            self, base64_url_processor(self.captcha.image), self.__captcha
        )
        self.scene.captcha_entry.focus()

    def __captcha(self, captcha: str):
        self.scene.destroy()
        self.scene = LoadingScene(self)
        self.update()
        try:
            self.user = self.eventloop.run_until_complete(self.captcha.resolve(captcha))
            self.info = self.eventloop.run_until_complete(self.user.info())
        except Exception as err:
            self.scene.destroy()
            self.scene = ErrorScene(self, str(err))
            return
        self.scene.destroy()
        self.scene = ResultScene(self)
        print(
            f"Tal-token: {self.user.tal_token}\nXes-Rfh: {self.user.xes_rfh}\n个人信息:\n\n{repr(self.info)}"
        )
        return

    def __entry(self):
        self.scene = LoginScene(self, self.__login)
        self.scene.username_entry.focus()

    def __init__(self, eventloop: asyncio.AbstractEventLoop):
        super().__init__()
        self.eventloop = eventloop
        self.user = self.captcha = None
        self.title("XesAPIExtended utility")
        self.geometry("300x150")
        self.resizable(False, False)
        self.__entry()

if __name__ == "__main__":
    app = App(asyncio.new_event_loop())
    app.mainloop()
