from requests import get

from config import RV_LINK


def get_incidents_list(limit: int,
                       fields: dict | None=None,
                       filter: dict | None=None,
                       sort: dict | None=None,
                       offset: int=0) -> dict:
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
    payload = {'limit': limit,
               'fields': fields,
               'filter': [{"property": filter['filter_name'],
                           "operator": filter['filter_operator'],
                           "value": filter['filter_value']}],
               'sort': [{"property": sort['sort_field'],
                         "direction": sort['sort_direction']}],
               'offset': offset}

    response = get(f'https://{RV_LINK}/api/v2/incidents/', params=payload)

    return response.json()
