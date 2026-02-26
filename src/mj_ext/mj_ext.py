import time
from datetime import datetime, timedelta, timezone

from mailjet_rest import Client

from mj_ext.models import MailjetContact, MailjetMessage
from mj_ext.utils import raise_for_status


def get_msg_status(mj_client: Client, msg_id: int) -> str:
    result = mj_client.message.get(id=msg_id)
    raise_for_status(result)

    data = result.json()["Data"]

    if len(data) > 1:
        return "ambiguous respnse (more than one message with same id)"

    return data[0]["Status"]


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
        ArrivedAt=msg["ArrivedAt"],
        ContactID=msg["ContactID"],
        MessageID=msg["ID"],
        SenderID=msg["SenderID"],
        Subject=msg["Subject"],
        Status=msg["Status"],
    )


def get_contact(mj_client: Client, contact_id: int) -> dict:
    result = mj_client.contact.get(id=contact_id)
    raise_for_status(result)

    return result.json()["Data"][0]


def condense_contact(contact: dict) -> MailjetContact | None:
    if not contact:
        return None

    return MailjetContact(
        ContactID=contact["ID"],
        Email=contact["Email"],
        Name=contact["Name"],
    )
