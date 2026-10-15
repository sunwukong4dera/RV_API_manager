from time import sleep

from get_another_incidents import check_applicants_from_filtered
from incidents import get_incidents_list
from config import BASE_INCIDENTS_COUNT_FOR_CHECK_TO_BIND, BASE_INCIDENT_FIELDS, BASE_INCIDENT_NOT_CLOSE_FILTER


def search_incident():
    print('Цикл запущен...')
    while True:
        print('=== Новая итерация ===')
        incidents_raw_dict = get_incidents_list(limit=BASE_INCIDENTS_COUNT_FOR_CHECK_TO_BIND,
                                                fields=BASE_INCIDENT_FIELDS,
                                                filter=BASE_INCIDENT_NOT_CLOSE_FILTER)
        data = incidents_raw_dict.get('data')
        incidents_list: list = data.get('result')

        for incident in incidents_list:
            print('Инцидент для связывания:', incident)
            company = incident.get('company')
            company_id = company.get('id')

            description = incident.get('description')

            incident_owner = incident.get('incident_owner')
            incident_owner_id = incident_owner.get('id')
            if incident_owner_id is not None:
                print(' - ответственный (id):', incident_owner_id) # todo забрать инфу из активов об пользаке и его теге
            else:
                print(' - нет ответственного')
            print('Начало проверки...')

            filters_for_applicants = [
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
            applicants_list: list = check_applicants_from_filtered(filters_for_applicants=filters_for_applicants)

        sleep(60)
