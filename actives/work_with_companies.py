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
                   verify=RV_CERT,
                   timeout=10)

    response.raise_for_status()
    print(response.url)

    return response.json()

if __name__ == '__main__':
    result = get_companies_list(limit=100)

    with open('companies.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
