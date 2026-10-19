import logging
from time import sleep
from datetime import datetime

from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException

from get_another_incidents import check_applicants_from_filtered
from incidents import get_incidents_list
from config import (
    BASE_INCIDENTS_COUNT_FOR_CHECK_TO_BIND,
    BASE_INCIDENT_FIELDS,
    BASE_INCIDENT_CREATED_FILTER,
    REFRESH_RATE
)
from extending_filters import extend_filter_for_applicants
from util import extend_filter_last_24_hours, get_incident_results

logger = logging.getLogger(__name__)


def search_incident(
    allow_bond_without_filter: bool=True
) -> None:
    """
    функция регулярно (каждые REFRESH_RATE секунд)

    :param allow_bond_without_filter: связывать инциденты без установленного отдельного фильтра (по умолчанию True)
    :return:
    """
    refresh_rate = int(REFRESH_RATE)
    logger.info('Цикл запущен...')
    while True:
        logger.info('=== Новая итерация ===')
        try:
            incidents_raw_dict = get_incidents_list(limit=BASE_INCIDENTS_COUNT_FOR_CHECK_TO_BIND,
                                                    fields=BASE_INCIDENT_FIELDS,
                                                    filter=extend_filter_last_24_hours(BASE_INCIDENT_CREATED_FILTER))
            incidents_list = get_incident_results(incidents_raw_dict)

            for incident in incidents_list:
                if not isinstance(incident, dict):
                    logger.warning('Пропуск карточки: ожидался словарь')
                    continue
                company = incident.get('company')
                if not isinstance(company, dict) or company.get('id') is None:
                    logger.warning(f"Пропуск {incident.get('identifier')}: нет организации")
                    continue
                company_id = company['id']

                externalid = incident.get('externalid')
                identifier = incident.get('identifier')
                if not identifier or not externalid:
                    logger.warning('Пропуск карточки: нет identifier или externalid')
                    continue
                try:
                    datetime.strptime(incident['creation'], "%Y-%m-%dT%H:%M:%S.%fZ")
                except (KeyError, TypeError, ValueError):
                    logger.warning(f'Пропуск {identifier}: неверная дата creation')
                    continue
                logger.info('%s %s', 'Инцидент для связывания:', incident)

                incident_owner = incident.get('incident_owner')
                if isinstance(incident_owner, dict):
                    incident_owner_id = incident_owner.get('id')
                    if incident_owner_id is not None:
                        logger.info('%s %s', ' - ответственный (id):', incident_owner_id) # todo использовать актив уведомлений (?)
                    else:
                        logger.info(' - нет ответственного')
                logger.info('Начало проверки...')

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

                try:
                    extended_filters_for_applicants = extend_filter_for_applicants(
                        filters_for_applicants=filters_for_applicants
                    )
                except (OSError, ValueError) as error:
                    logger.error(f'Ошибка файла дополнительных правил: {error}. Обработка остановлена.')
                    return

                if not allow_bond_without_filter and extended_filters_for_applicants == filters_for_applicants:
                    continue

                applicants_list: list = check_applicants_from_filtered(
                    filters_for_applicants=extended_filters_for_applicants,
                    current_incident=incident
                )
        except (Timeout, ConnectionError) as error:
            logger.error(f'Ошибка соединения ({type(error).__name__}). Повтор после паузы.')
        except HTTPError as error:
            status = error.response.status_code if error.response is not None else None
            logger.error(f'HTTP-ошибка: {status}')
            if status != 429 and (status is None or not 500 <= status < 600):
                logger.error('Проверьте параметры запроса, авторизацию и права. Обработка остановлена.')
                return # скорее всего системка
        except ValueError as error:
            logger.error(f'Ошибка ответа API: {error}. Текущий проход прерван.')
        except RequestException as error:
            logger.error(f'Ошибка запроса ({type(error).__name__}). Обработка остановлена.')
            return # скорее всего системка

        sleep(refresh_rate)
