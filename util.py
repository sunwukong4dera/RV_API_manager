import json
from datetime import datetime


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
