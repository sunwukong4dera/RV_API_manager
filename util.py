import json
from datetime import datetime

from config import API_RESPONSES


def write_to_file(data) -> None:
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"incidents_{current_time}.json"

    with open(f'../{API_RESPONSES}{filename}', 'w', encoding='utf-8') as f:
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
