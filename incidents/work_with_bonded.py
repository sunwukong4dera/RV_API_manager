from requests import post
from urllib.parse import unquote

from config import RV_LINK, TOKEN, RV_CERT


def add_bonded_incident(uuid_incident: str) -> dict:
    """

    :param uuid_incident: - uuid-идентификатор инцидента
    :return:
    """
    headers = {
        'X-Token': TOKEN
    }

    payload: dict = {'uuid_incident': uuid_incident}

    response = post(f'https://{RV_LINK}/api/v2/incidents/',
                   headers=headers,
                   params=payload,
                   verify=RV_CERT,
                   timeout=10)

    response.raise_for_status()
    print(unquote(response.url))

    return response.json()
