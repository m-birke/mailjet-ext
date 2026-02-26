from enum import Enum

from pydantic import BaseModel


class MailjetMsgStatus(Enum):
    UNKNOWN = ("unknown", 0)
    QUEUED = ("queued", 1)
    SENT = ("sent", 2)
    OPENED = ("opened", 3)
    CLICKED = ("clicked", 4)
    BOUNCE = ("bounce", 5)
    SPAM = ("spam", 6)
    UNSUB = ("unsub", 7)
    BLOCKED = ("blocked", 8)
    SOFTBOUNCED = ("softbounced", 9)
    HARDBOUNCED = ("hardbounced", 10)
    DEFERRED = ("deferred", 11)

    def __init__(self, text, code):
        self.text = text
        self.code = code


class MailjetMessage(BaseModel):
    ArrivedAt: str
    ContactID: int
    MessageID: int
    SenderID: int
    Subject: str
    Status: str


class MailjetContact(BaseModel):
    ContactID: int
    Email: str
    Name: str
