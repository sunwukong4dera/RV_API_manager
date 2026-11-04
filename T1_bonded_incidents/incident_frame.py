import pandas as pd


SEVERITY_ORDER = {'high': 0, 'medium': 1, 'low': 2}


def prepare_incident_frame(incidents: list[dict]) -> pd.DataFrame:
    """Готовит кандидатов одной компании для дальнейшей проверки правил.

    Ожидается формат API: level = {'id': ..., 'name': 'High/Medium/Low'},
    creation — дата ISO 8601. Исходные поля сохраняются, creation становится
    datetime в UTC, severity_rank задаёт порядок критичности: 0, 1, 2.
    Сначала high, затем medium, low; внутри уровня — самые старые первыми.
    Компания и допустимое временное окно уже отобраны вызывающим кодом.
    """
    frame = pd.DataFrame(incidents)
    if frame.empty:
        return frame

    frame['creation'] = pd.to_datetime(frame['creation'], utc=True)
    frame['severity_rank'] = frame['level'].str.get('name').str.lower().map(SEVERITY_ORDER)

    return frame.sort_values(
        ['severity_rank', 'creation', 'identifier'],
        ascending=True,
    ).reset_index(drop=True)
