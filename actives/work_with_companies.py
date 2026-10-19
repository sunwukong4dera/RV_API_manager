import json

from requests import get

from config import RV_LINK, RV_TOKEN, RV_CERT_PATH


def get_companies_list(limit: int,
                       fields: list | None=None,
                       filter: dict | None=None,
                       sort: dict | None=None,
                       start: int | None=None) -> dict:
    """
    require:
    :param limit:

    пример:
        get_companies_list(limit=100, fields=['id', 'name'])

    not require:
    :param fields:
    :param filter:
    :param sort:
    :param start:

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
        filter = json.dumps([
            {
                "property": filter["filter_name"],
                "operator": filter["filter_operator"],
                "value": filter["filter_value"],
            }
        ])
    headers = {
        'X-Token': RV_TOKEN,
        "Content-Type": "application/json"
    }

    payload: dict = {'limit': limit,
               'fields': fields,
               'filter': filter,
               'sort': sort,
               'offset': start}

    response = get(f'https://{RV_LINK}/api/v2/companies/',
                   headers=headers,
                   params=payload,
                   verify=RV_CERT_PATH,
                   timeout=10)

    response.raise_for_status()
    print(response.url)

    return response.json()
