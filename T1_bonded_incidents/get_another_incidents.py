import logging
from incidents import get_incidents_list
from datetime import datetime

from util import get_oldest, get_incident_results
from config import BASE_INCIDENTS_COUNT_FOR_CHECK_TO_APPLICANT, BASE_INCIDENT_FIELDS

logger = logging.getLogger(__name__)


def check_applicants_from_filtered(
        filters_for_applicants: list[dict],
        current_incident: dict,
) -> list:
    """
    ручная проверка, подбор всех кондидатов по фильтрам, заданным по основному инциденту

    + дополнительные фильтры + дополнительная проверка РЕАЛИЗОВАНЫ с помощью дополнения фильтра текущего инцидента
        по его уникальному ключу "контракт.правило". Для уникализации функционала возможно потребуется расширение
        пространства имен ключей на версии или отдельные файлы-ключи.
    + связывание инцидента по post РЕАЛИЗОВАНО но не проверено потому что у текущего ключа нет прав (?)

    :param current_incident: текущая карточка из основного списка
    :param filters_for_applicants: фильтр, переданный по текущему инциденту
    :return:
    """

    applicants_from_filtered_raw_dict: dict = get_incidents_list(
        limit=BASE_INCIDENTS_COUNT_FOR_CHECK_TO_APPLICANT,
        fields=BASE_INCIDENT_FIELDS,
        filter=filters_for_applicants
    )

    applicants_list = get_incident_results(applicants_from_filtered_raw_dict)
    current_identifier = current_incident['identifier']
    current_creation = datetime.strptime(current_incident['creation'], "%Y-%m-%dT%H:%M:%S.%fZ")

    applicants_except_current = []
    for incident in applicants_list:
        if not isinstance(incident, dict) or not incident.get('identifier'):
            logger.warning('Пропуск кандидата: нет идентификатора')
            continue
        if incident['identifier'] == current_identifier:
            continue
        try:
            creation = datetime.strptime(incident['creation'], "%Y-%m-%dT%H:%M:%S.%fZ")
        except (KeyError, TypeError, ValueError):
            logger.warning(f"Пропуск кандидата {incident['identifier']}: неверная дата creation")
            continue
        if creation < current_creation:
            applicants_except_current.append(incident)

    oldest = get_oldest(applicants_except_current)

    logger.info(f'Проверка кандидатов для: {current_identifier}\n'
        f' - указанные фильтры: {[f.get("value") for f in filters_for_applicants]}\n'
        f' - длина списка кандидатов: {len(applicants_except_current)}\n'
        f' - старейший кандидат: {oldest}\n')

    return applicants_except_current
