from incidents import get_incidents_list
from util import get_oldest
from config import BASE_INCIDENTS_COUNT_FOR_CHECK_TO_APPLICANT, BASE_INCIDENT_FIELDS


def check_applicants_from_filtered(
        filters_for_applicants: list[dict],
        current_identifier: str,
) -> list:
    """
    ручная проверка, подбор всех кондидатов по фильтрам, заданным по основному инциденту

    + дополнительные фильтры + дополнительная проверка РЕАЛИЗОВАНЫ с помощью дополнения фильтра текущего инцидента
        по его уникальному ключу "контракт.правило". Для уникализации функционала возможно потребуется расширение
        пространства имен ключей на версии или отдельные файлы-ключи.
    + связывание инцидента по post РЕАЛИЗОВАНО но не проверено потому что у текущего ключа нет прав (?)

    :param current_identifier: идентификатор текущего инцидента
    :param filters_for_applicants: фильтр, переданный по текущему инциденту
    :return:
    """

    applicants_from_filtered_raw_dict: dict = get_incidents_list(
        limit=BASE_INCIDENTS_COUNT_FOR_CHECK_TO_APPLICANT,
        fields=BASE_INCIDENT_FIELDS,
        filter=filters_for_applicants
    )

    applicants_from_filtered_data = applicants_from_filtered_raw_dict.get('data')
    applicants_list: list = applicants_from_filtered_data.get('result')

    current_incident = next(
        (
            incident for incident in applicants_list
            if incident.get('identifier') == current_identifier
        ),
        None
    )

    if current_incident is None:
        print(f'Инцидент {current_identifier} не найден')
        return []

    applicants_except_current = [
        incident for incident in applicants_list
        if incident.get('identifier') != current_identifier
        and incident['creation'] < current_incident['creation']
    ]

    oldest = get_oldest(applicants_except_current)

    print(
        f'Проверка кандидатов для: {current_identifier}\n'
        f' - указанные фильтры: {[f.get("value") for f in filters_for_applicants]}\n'
        f' - длина списка кандидатов: {len(applicants_except_current)}\n'
        f' - старейший кандидат: {oldest}\n'
    )

    return applicants_except_current
