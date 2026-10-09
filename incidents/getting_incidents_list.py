import json

from requests import get

from config import RV_LINK, TOKEN, RV_CERT


def get_incidents_list(limit: int,
                       fields: list | str | None=None,
                       filter: dict | None=None,
                       sort: dict | None=None,
                       offset: int | None=None) -> dict:
    """
    require:
    :param limit:

    not require:
    :param fields:
    :param filter:
    :param sort:
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
               'offset': offset}

    response = get(f'https://{RV_LINK}/api/v2/incidents/',
                   headers=headers,
                   params=payload,
                   verify=RV_CERT,
                   timeout=10)

    response.raise_for_status()
    print(response.url)
    # https://rv-soar-app.jetcsirt.loc/api/v2/incidents/?limit=10&fields=type%2Cincident_uuid%2Cidentifier%2Cincident_owner&offset=0
    # https://rv-soar-app.jetcsirt.loc/api/v2/companies/?limit=100
    # https://rv-soar-app.jetcsirt.loc/api/v2/incidents/?limit=10

    return response.json()


if __name__ == '__main__':
    result = get_incidents_list(limit=10)

    with open('incidents.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        # , offset=0, fields=["type", "incident_uuid", "identifier", "incident_owner"]
