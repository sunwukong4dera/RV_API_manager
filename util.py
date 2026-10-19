import json
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
        current_filters: list | None = next(
            (i.get(composite_identifier) for i in data)
            , None
        )
        return current_filters


def extend_filter_last_24_hours(current_filters: list) -> list:
    last_24_hours = (
            datetime.now(timezone.utc) - timedelta(hours=24)
    ).isoformat(timespec="milliseconds").replace("+00:00", "Z")

    filter_last_24_hours = [
        {
            "property": "creation",
            "operator": ">=",
            "value": last_24_hours
        }
    ]
    new_filters = current_filters
    new_filters.extend(filter_last_24_hours)

    return new_filters
