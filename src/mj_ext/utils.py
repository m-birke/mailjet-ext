from mailjet_rest import Client
from mailjet_rest.client import ApiError

_MAILJET_API_VERSION = "v3"
_HTTP_STATUS_OK = 200


def init_mailjet_client(api_key: str, api_secret: str) -> Client:
    return Client(auth=(api_key, api_secret), version=_MAILJET_API_VERSION)


def test_connection(api_key: str, api_secret: str) -> None:
    """Tests the connection to mailjet by sending a request to the send endpoint.

    :param api_key: The API key for Mailjet
    :param api_secret: The API secret for Mailjet
    """
    mj = init_mailjet_client(api_key=api_key, api_secret=api_secret)
    try:
        response = mj.send.get()
    except ApiError as e:
        print(f"Failed with exception: {e}")  # noqa T201
        return

    if response.status_code == 405 and response.json()["ErrorMessage"].startswith("Method GET not allowed"):  # noqa PLR2004
        print("Success")  # noqa T201
        return

    print(f"Status Code: {response.status_code}, Response: {response.text}")  # noqa T201


def raise_for_status(response) -> None:
    if response.status_code != _HTTP_STATUS_OK:
        raise ApiError(response.status_code, response.reason, response.text)
