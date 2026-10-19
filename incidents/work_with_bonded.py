import logging
from requests import post
from urllib.parse import unquote

from config import RV_LINK, RV_TOKEN, RV_CERT_PATH

logger = logging.getLogger(__name__)


def add_bonded_incident(current_incident_uuid: str, incident_uuid: str) -> dict:
    """
    :param current_incident_uuid: - uuid-идентификатор инцидента, который мы подвязываем
    :param incident_uuid: - uuid-идентификатор инцидента, который мы подвязываем
    :return:
    """
    url = f'https://{RV_LINK}/api/v2/incidents/{current_incident_uuid}/incidents/'

    headers = {
        'X-Token': RV_TOKEN,
        "Content-Type": "application/json"
    }

    payload: dict = {
        'incident_uuid': incident_uuid
    }

    response = post(url=url,
                   headers=headers,
                   params=payload,
                   verify=RV_CERT_PATH,
                   timeout=10)

    response.raise_for_status()
    logger.info(unquote(response.url))

    return response.json()
