from datetime import datetime
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
    arrived_at: str
    contact_id: int
    message_id: int
    sender_id: int
    subject: str
    status: str


class MailjetContact(BaseModel):
    contact_id: int
    email: str
    name: str


class MailjetMsgHistoryEvents(Enum):
    SENT = "sent"
    OPENED = "opened"
    CLICKED = "clicked"
    BOUNCED = "bounced"
    SOFTBOUNCED = "softbounced"
    HARDBOUNCED = "hardbounced"
    BLOCKED = "blocked"
    UNSUBSCRIBED = "unsub"
    SPAM = "spam"


class MailjetMsgHistoryEvent(BaseModel):
    event: MailjetMsgHistoryEvents
    timestamp: datetime
