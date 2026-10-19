import logging
import json

from requests import get
from urllib.parse import unquote

from config import RV_LINK, RV_TOKEN, RV_CERT_PATH

logger = logging.getLogger(__name__)


def get_incidents_list(limit: int,
                       fields: list | str | None=None,
                       filter: list | None=None,
                       sort: dict | None=None,
                       offset: int | None=None) -> dict:
    """
    require:
    :param limit:

    not require:
    :param fields: поля инцидента
    :param filter: фильтр по которому будут выводиться инциденты (по умолчанию operator: '=')
    :param sort: сортировка инцидентов
    :param offset:

    :return: json response
    """
    if type(fields) is list:
        fields = ','.join(fields)

    if sort is not None:
        sort = json.dumps([
            {
                "property": sort['sort_field'],
                "direction": sort['sort_direction']
            }
        ])

    if filter is not None:
        filter = json.dumps(filter)

    headers = {
        "X-Token": RV_TOKEN,
        "Content-Type": "application/json"
    }

    payload: dict = {'limit': limit,
               'fields': fields,
               'filter': filter,
               'sort': sort,
               'offset': offset}

    response = get(f'https://{RV_LINK}/api/v2/incidents/',
                   headers=headers,
                   params=payload,
                   verify=RV_CERT_PATH,
                   timeout=10)

    response.raise_for_status()
    logger.info('%s %s', 'ЗАПРОС:', unquote(response.url))

    return response.json()
