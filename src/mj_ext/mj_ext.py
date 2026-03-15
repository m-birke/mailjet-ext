import time
from datetime import datetime, timedelta, timezone

from mailjet_rest import Client

from mj_ext.models import MailjetContact, MailjetMessage, MailjetMsgHistoryEvent
from mj_ext.utils import raise_for_status

_MSG_STATUS_JSON_FIELD_NAME = "Status"


def get_msg(mj_client: Client, msg_id: int) -> dict:
    result = mj_client.message.get(id=msg_id)
    raise_for_status(result)

    data = result.json()["Data"]

    if len(data) > 1:
        msg = "Ambiguous response (more than one message with same id)"
        raise ValueError(msg)

    return data[0]


def get_msg_status(mj_client: Client, msg_id: int) -> str:
    return get_msg(mj_client=mj_client, msg_id=msg_id)[_MSG_STATUS_JSON_FIELD_NAME]


def get_msgs_per_status(mj_client: Client, days_into_past: int, status: int) -> list[MailjetMessage | None]:
    from_ts = int(time.mktime((datetime.now(timezone.utc) - timedelta(days=days_into_past)).timetuple()))
    to_ts = int(time.mktime(datetime.now(timezone.utc).timetuple()))

    filters = {
        "MessageStatus": status,
        "FromTS": from_ts,
        "ToTS": to_ts,
    }

    result = mj_client.message.get(filters=filters)
    raise_for_status(result)

    return [condense_msg(msg) for msg in result.json()["Data"]]


def condense_msg(msg: dict) -> MailjetMessage | None:
    if not msg:
        return None

    return MailjetMessage(
        arrived_at=msg["ArrivedAt"],
        contact_id=msg["ContactID"],
        message_id=msg["ID"],
        sender_id=msg["SenderID"],
        subject=msg["Subject"],
        status=msg["Status"],
    )


def get_msg_history(mj_client: Client, msg_id: int) -> list[dict]:
    result = mj_client.messagehistory.get(id=msg_id)
    raise_for_status(result)

    return result.json()["Data"]


def parse_msg_history(msg_history: list[dict]) -> list[MailjetMsgHistoryEvent]:
    return [
        MailjetMsgHistoryEvent(event=el["EventType"], timestamp=datetime.fromtimestamp(el["EventAt"], timezone.utc))
        for el in msg_history
    ]


def get_contact(mj_client: Client, contact_id: int) -> dict:
    result = mj_client.contact.get(id=contact_id)
    raise_for_status(result)

    return result.json()["Data"][0]


def condense_contact(contact: dict) -> MailjetContact | None:
    if not contact:
        return None

    return MailjetContact(
        contact_id=contact["ID"],
        email=contact["Email"],
        name=contact["Name"],
    )
