from incidents import get_incidents_list
from util import write_to_file


def main():
    # получение инцидентов только по компании
    filter_company = [
        {
            "property": "company",
            "operator": "=",
            "value": 58
        }
    ]

    # получение инцидентов только по пользователю
    filter_owner = [
        {
            "property": "incident_owner",
            "operator": "=",
            "value": 421
        }
    ]

    # получение инцидентов по пользователю и компании
    filters_owner_company = [
        {
            "property": "incident_owner",
            "operator": "=",
            "value": 421
        },
        {
            "property": "company",
            "operator": "=",
            "value": 58
        }
    ]

    incident_fields = [
        "incident_uuid",
        "identifier",
        "type",
        "company",
        "incident_owner",
        "status"
    ]

    result = get_incidents_list(limit=10, fields=incident_fields, filter=filters_owner_company)
    write_to_file(result)


if __name__ == '__main__':
    main()
