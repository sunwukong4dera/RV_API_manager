import logging

from config import BASE_INCIDENT_NOT_CLOSE_FILTER, HOURS_FINDING
from util import extend_filter_last_n_hours, get_incident_results
from .get_another_incidents import check_applicants_from_filtered


logger = logging.getLogger(__name__)


def explore_incident(incident: dict):
    identifier, company = incident['identifier'], incident['company']
    if not isinstance(company, dict) or company.get('id') is None:
        raise ValueError(f"Ошибка {identifier}: нет организации")
    company_id = company['id']
    logger.info(f"=== Инцидент {identifier} получен. ID компании: {company_id}")

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
    logger.info(f'=== Длина списка кандидатов для {identifier}: {len(applicants)}; '
                f'Кандидаты (первые 10): {", ".join(list(i["identifier"] for i in applicants if i is not None)[:10])}')

    return company_id, applicants
