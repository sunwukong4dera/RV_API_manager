from incidents import get_incidents_list
from util import get_latest


def check_applicants_from_filtered(filters: list[dict]) -> list:
    """
    ручная проверка

    :param filters:
    :return:
    """
    applicants_from_filtered_raw_dict: dict = get_incidents_list(limit=100, filter=filters)
    applicants_from_filtered_data = applicants_from_filtered_raw_dict.get('data')
    applicants_from_filtered_list: list = applicants_from_filtered_data.get('result')

    print(f'filters: {(filter.get("value") for filter in filters)}\n'
          f'len of applicants list: {len(applicants_from_filtered_list)}\n'
          f'the most late: {get_latest(applicants_from_filtered_list)}\n'
          f'{applicants_from_filtered_list}')

    return applicants_from_filtered_list


