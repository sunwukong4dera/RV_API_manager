import json

from incidents import get_incidents_list


def get_another(filter: list[dict]) -> dict:
    another_incidents_list = get_incidents_list(limit=10, filter=filter)
    return another_incidents_list


def main() -> None:
    """
    вызывается функиця которая по полям уже известного инцидента проверяет другие по орге и идентификатору
    и находит по правилу (например одинаковая цель)

    :return:
    """
    filters = [
        {
            "property": "incident_owner",
            "operator": "=",
            "value": 421
        },
        {
            "property": "company",
            "operator": "=",
            "value": 58
        },
        {
            "property": "type",
            "operator": "=",
            "value": 31
        },
        {
            "property": "status",
            "operator": "!=",
            "value": 62
        }
    ]
    get_another(filters)


if __name__ == "__main__":
    main()
