from incidents import get_incidents_list
from util import get_oldest
from config import BASE_INCIDENTS_COUNT_FOR_CHECK_TO_APPLICANT, BASE_INCIDENT_FIELDS


def check_applicants_from_filtered(filters_for_applicants: list[dict]) -> list:
    """
    ручная проверка, подбор всех кондидатов по фильтрам, заданным по основному инциденту

    # todo дополнительные фильтры + дополнительная проверка;
    # todo связывание инцидента по post

    :param filters_for_applicants:
    :return:
    """
    applicants_from_filtered_raw_dict: dict = get_incidents_list(limit=BASE_INCIDENTS_COUNT_FOR_CHECK_TO_APPLICANT,
                                                                 fields=BASE_INCIDENT_FIELDS,
                                                                 filter=filters_for_applicants)
    applicants_from_filtered_data = applicants_from_filtered_raw_dict.get('data')
    applicants_list: list = applicants_from_filtered_data.get('result')

    applicants_first, applicants_except_first = applicants_list[0], applicants_list[1:]
    oldest = get_oldest(applicants_except_first)

    print(f'Проверка кандидатов для: {applicants_first.get("identifier")}\n'
          f' - указанные фильтры: {list((filter.get("value") for filter in filters_for_applicants))}\n'
          f' - длина списка кандидатов: {len(applicants_except_first)}\n'
          f' - старейший кандидат: {oldest}\n')

    return applicants_list
