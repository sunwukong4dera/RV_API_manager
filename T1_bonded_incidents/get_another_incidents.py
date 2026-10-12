import json

from incidents import get_incidents_list


def make_filter(values: dict):
    final_list = []
    for key, value in values.items():
        if type(value) is not list:
            final_list.append({
                "property": key,
                "value": value
            })
            continue
        final_list.append({
            "property": key,
            "filter_operator": "in",
            "value": value
        })

    json.dumps(values)


def get_another(values: dict):
    filter = make_filter(values)
    incidents_list = get_incidents_list(limit=10, filter=filter)
    return incidents_list


"""
if __name__ == "__main__":
    values = {
        "externalid": "JC-NAA-016-002",
        "company": {
            "id": 42
        },
        "final_classification": None
    }
    get_another(values)
"""
