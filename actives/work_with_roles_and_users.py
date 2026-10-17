import json

from urllib.parse import unquote

from general_function import get_asset_data
from config import ASSET_ID_USERS


def get_users(limit: int,
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
    :param filter: фильтр по которому будут выводиться пользователи (по умолчанию operator: '=')
    :param sort: сортировка инцидентов
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
                              asset_type_id=ASSET_ID_USERS
                              )

    print('ЗАПРОС:', unquote(response.url))

    return response.json()
