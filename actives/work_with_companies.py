import json

from requests import get

from config import RV_LINK, TOKEN, RV_CERT


def get_companies_list(limit: int,
                       fields: list | None=None,
                       filter: dict | None=None,
                       sort: dict | None=None,
                       start: int | None=None) -> dict:
    """
    require:
    :param limit:

    not require:
    :param fields:
    :param filter:
    :param sort:
    :param start:

    :return: json response
    """
    if sort is None:
        sort = {}
    else:
        sort = [{"property": sort['sort_field'], "direction": sort['sort_direction']}]

    if filter is None:
        filter = {}
    else:
        filter = [{"property": filter['filter_name'],
                  "operator": filter['filter_operator'],
                  "value": filter['filter_value']}]

    headers = {
        'X-Token': TOKEN
    }

    payload: dict = {'limit': limit,
               'fields': fields,
               'filter': filter,
               'sort': sort,
               'offset': start}

    response = get(f'https://{RV_LINK}/api/v2/companies/',
                   headers=headers,
                   params=payload,
                   verify=RV_CERT)

    print(response.url)

    return response.json()


with open('companies.json', 'w', encoding='utf-8') as f:
    json.dump(get_companies_list(limit=100), f, ensure_ascii=False, indent=2)
