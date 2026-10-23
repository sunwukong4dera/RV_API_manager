import json
import logging
from pathlib import Path
from datetime import datetime, timedelta, timezone


def write_to_json_file(filename: str, data) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_oldest(incidents: list[dict]) -> dict | None:
    if not incidents:
        return None

    return min(
        incidents,
        key=lambda incident: datetime.strptime(
            incident["creation"],
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
    )


def get_extend_filter(filename: str, company: int, externalid: str) -> list | None:
    composite_identifier = f'{company}.{externalid}'
    with open(filename, 'r', encoding='utf-8') as f:
        data: list = json.load(f)
        if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
            raise ValueError('Файл правил должен содержать список словарей')
        current_filters: list | None = next(
            (i[composite_identifier] for i in data if composite_identifier in i)
            , None
        )
        if current_filters is not None and (
            not isinstance(current_filters, list)
            or any(not isinstance(item, dict)
            or not {'property', 'value'} <= item.keys()
            for item in current_filters)
        ):
            raise ValueError(f'Неверный формат правила {composite_identifier}')
        return current_filters


def extend_filter_last_n_hours(current_filters: list, hours: int) -> list:
    last_n_hours = (
            datetime.now(timezone.utc) - timedelta(hours=hours)
    ).isoformat(timespec="milliseconds").replace("+00:00", "Z")

    filter_last_n_hours = [
        {
            "property": "creation",
            "operator": ">=",
            "value": last_n_hours
        }
    ]
    new_filters = current_filters.copy()
    new_filters.extend(filter_last_n_hours)

    return new_filters


def get_incident_results(response: dict) -> list:
    if not isinstance(response, dict) or response.get('success') is not True:
        raise ValueError('API не подтвердил успешное выполнение запроса')
    data = response.get('data')
    if not isinstance(data, dict) or not isinstance(data.get('result'), list):
        raise ValueError('В ответе API отсутствует список data.result')
    return data['result']


def setup_logging() -> Path:
    logs_directory = Path(__file__).resolve().parent / 'logs'
    logs_directory.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
    log_path = logs_directory / f'incident_binding_{started_at}.log'

    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    console_handler = logging.StreamHandler()
    for handler in (file_handler, console_handler):
        handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
        force=True,
    )
    return log_path
