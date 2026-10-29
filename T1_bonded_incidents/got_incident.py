import logging

from incidents import get_incidents_list
from config import BASE_INCIDENT_FIELDS, BASE_INCIDENT_NOT_CLOSE_FILTER, HOURS_FINDING
from util import extend_filter_last_n_hours, get_incident_results
from .get_another_incidents import check_applicants_from_filtered


logger = logging.getLogger(__name__)


def explore_incident(identifier: str):
    current_identifier_filter = BASE_INCIDENT_NOT_CLOSE_FILTER.copy()
    # оставить для исключения изначально закрытых инцов
    current_identifier_filter.extend([
        {
            "property": "identifier",
            "operator": "=",
            "value": identifier
        }
    ])
    incident_raw_dict = get_incidents_list(
        limit=1,
        fields=BASE_INCIDENT_FIELDS,
        filter=current_identifier_filter
    )
    incident_list = get_incident_results(incident_raw_dict)

    incident = next(
        (inc for inc in incident_list),
        ValueError(f'Ошибка: инцидент {identifier} не найден')
    )

    if not isinstance(incident, dict):
        raise ValueError('Ошибка: ожидался словарь')
    company = incident.get('company')
    if not isinstance(company, dict) or company.get('id') is None:
        raise ValueError(f"Ошибка {identifier}: нет организации")
    company_id = company['id']

    filters_for_applicants = BASE_INCIDENT_NOT_CLOSE_FILTER.copy()
    filters_for_applicants.extend([
        {
            "property": "company",
            "operator": "=",
            "value": company_id
        }
    ])

    applicants: list = check_applicants_from_filtered(
        filters_for_applicants=extend_filter_last_n_hours(filters_for_applicants, int(HOURS_FINDING)),
        current_incident=incident,
    )
    logger.info(f'Длина списка кандидатов для {identifier}: {len(applicants)};'
                f'Кандидаты: {str(*(i.get("identifier") for i in applicants if i is not None))}')

    return company_id, applicants
