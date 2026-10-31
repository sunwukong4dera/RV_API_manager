import logging
import json

from urllib.parse import unquote

from actives import get_asset_data
from config import ASSET_BINDING_RULES


logger = logging.getLogger(__name__)


def get_binding_rules(limit: int,
              fields: list | str | None=None,
              filter: list | None=None,
              sort: dict | None=None,
              start: int | None=None
              ) -> dict:
    """
    require:
    :param limit:

    not require:
    :param fields: поля инцидента
    :param filter: фильтр по которому будут выводиться правила (по умолчанию operator: '=')
    :param sort: сортировка правил
    :param start: порядковый номер первой записи, начиная с которой выводится ответ (offset)

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

    payload: dict = {
        'limit': limit,
        'fields': fields,
        'filter': filter,
        'sort': sort,
        'start': start
    }

    response = get_asset_data(request_params=payload,
                              asset_type_id=ASSET_BINDING_RULES
                              )

    logger.info('%s %s', 'ЗАПРОС:', unquote(response.url))

    return response.json()
