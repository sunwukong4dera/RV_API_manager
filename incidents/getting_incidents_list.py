from requests import get

from config import RV_LINK


payload = {'fields': '<fields>',
           'filter': [{"property":"<filter_name>", "operator":"<filter_operator>", "value":"<filter_value>"}],
           'sort':[{"property": "<sort_field>", "direction":"<sort_direction>"}],
           'limit': '<limit>',
           'offset': '<offset>'}
response = get(f'https://{RV_LINK}/api/v2/incidents/', params=payload)
print(response.json())
