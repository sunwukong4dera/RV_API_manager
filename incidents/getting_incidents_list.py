import json

from requests import get

from config import RV_LINK, TOKEN, RV_CERT


def get_incidents_list(limit: int,
                       fields: list | None=None,
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
               'offset': offset}

    response = get(f'https://{RV_LINK}/api/v2/incidents/',
                   headers=headers,
                   params=payload,
                   verify=RV_CERT)

    return response.json()


with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(get_incidents_list(limit=10, offset=10, fields=["type", "incident_uuid", "identifier", "incident_owner"]), f, ensure_ascii=False, indent=2)
