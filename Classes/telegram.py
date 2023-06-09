from textwrap import dedent

import requests


class Telegram(object):
    __slots__ = ["chat_id", "telegram_api", "events", "disable_notification"]

    def __init__(
        self, chat_id: int, token: str, disable_notification: bool = False
    ):
        self.chat_id = chat_id
        self.telegram_api = f"https://api.telegram.org/bot{token}/sendMessage"
        self.disable_notification = disable_notification
        

    def send(self, message: str) -> None:
  
        requests.post(
            url=self.telegram_api,
            data={
                "chat_id": self.chat_id,
                "text": dedent(message),
                "disable_web_page_preview": False,  # include link to twitch streamer?
                "disable_notification": self.disable_notification,  # no sound, notif just in tray
            },
        )
