from incidents import get_incidents_list
from util import write_to_file


def main():
    # получение инцидентов по пользователю и компании, только инциденты (Подозрение на инцидент (событие ИБ))
    # и не статус закрыт
    filters_owner_company = [
        {
            "property": "incident_owner",
            "operator": "=",
            "value": 421
        },
        {
            "property": "company",
            "operator": "=",
            "value": 10
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

    incident_fields = "incident_uuid,type_group,type,status,rel,identifier,description,company,company_id,category"

    result = get_incidents_list(limit=10, fields=incident_fields, filter=filters_owner_company)
    write_to_file(result)


if __name__ == '__main__':
    main()
