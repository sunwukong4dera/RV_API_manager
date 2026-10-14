from time import sleep

from get_another_incidents import check_applicants_from_filtered
from incidents import get_incidents_list

def search_incident(incidents: list):
    filters_open_inc = [
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
    while True:
        incidents_raw_dict = get_incidents_list(limit=10, filter=filters_open_inc)
        data = incidents_raw_dict.get('data')
        incidents_list: list = data.get('result')

        for incident in incidents_list:
            company = incident.get('company')
            company_id = company.get('id')

            description = incident.get('description')

            tg_tag = incident.get('tag')
            tg_tag_name = tg_tag.get('tag_name')


            filters = [
                {
                    "property": "company",
                    "operator": "=",
                    "value": company_id
                },
                {
                    "property": "description",
                    "operator": "=",
                    "value": description
                },
                {
                    "property": "status",
                    "operator": "!=",
                    "value": 62
                }
            ]

            applicants_list: list = check_applicants_from_filtered(filters=filters)




        sleep(60)










