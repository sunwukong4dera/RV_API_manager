from time import sleep

from get_another_incidents import check_applicants_from_filtered
from incidents import get_incidents_list
from config import (
    BASE_INCIDENTS_COUNT_FOR_CHECK_TO_BIND,
    BASE_INCIDENT_FIELDS,
    BASE_INCIDENT_CREATED_FILTER,
    REFRESH_RATE
)
from extending_filters import extend_filter_for_applicants
from util import extend_filter_last_24_hours


def search_incident(
    allow_bond_without_filter: bool=True
) -> list:
    """
    функция регулярно (каждые REFRESH_RATE секунд)

    :param allow_bond_without_filter: связывать инциденты без установленного отдельного фильтра (по умолчанию True)
    :return:
    """
    print('Цикл запущен...')
    while True:
        print('=== Новая итерация ===')
        incidents_raw_dict = get_incidents_list(limit=BASE_INCIDENTS_COUNT_FOR_CHECK_TO_BIND,
                                                fields=BASE_INCIDENT_FIELDS,
                                                filter=extend_filter_last_24_hours(BASE_INCIDENT_CREATED_FILTER))
        data = incidents_raw_dict.get('data')
        incidents_list: list = data.get('result')

        for incident in incidents_list:
            print('Инцидент для связывания:', incident)
            company = incident.get('company')
            company_id = company.get('id')

            externalid = incident.get('externalid')
            identifier = incident.get('identifier')

            incident_owner = incident.get('incident_owner')
            if incident_owner is not None:
                incident_owner_id = incident_owner.get('id')
                if incident_owner_id is not None:
                    print(' - ответственный (id):', incident_owner_id) # todo использовать актив уведомлений (?)
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
                    "property": "externalid",
                    "operator": "=",
                    "value": externalid
                },
                {
                    "property": "status",
                    "operator": "!=",
                    "value": 62
                },
                {
                    "property": "status",
                    "operator": "!=",
                    "value": 77
                },
            ]

            extended_filters_for_applicants = extend_filter_for_applicants(
                filters_for_applicants=filters_for_applicants
            )

            if not allow_bond_without_filter and extended_filters_for_applicants == filters_for_applicants:
                continue

            applicants_list: list = check_applicants_from_filtered(
                filters_for_applicants=extended_filters_for_applicants,
                current_identifier=identifier
            )

        sleep(int(REFRESH_RATE))
