import json
from datetime import datetime

from config import API_RESPONSES


def write_to_file(data):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"incidents_{current_time}.json"

    with open(f'../{API_RESPONSES}{filename}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
