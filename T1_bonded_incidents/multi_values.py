import pandas as pd


def has_multi_values(field: str, general_value, values: pd.Series) -> bool:
    """
    проверяем разделители в основном инциденте и у кандидатов
    """
    if field == 'externalid' or not isinstance(general_value, str):
        return False
    if any(separator in general_value for separator in (',', '\n', '\r')):
        return True
    return bool(values.astype('string').str.contains(r'[,\r\n]', na=False).any())


def split_multi_values(value: str | None) -> set[str]:
    """
    разбиваем строку на отдельные значения
    """
    parts = value.replace(',', '\n').splitlines()
    multi_values = {
        part.strip() for part in parts if part.strip()
    }
    return multi_values


def multi_value_mask(general_value: str | None, values: pd.Series) -> pd.Series:
    """
    ищем хотя бы одно общее значение с основным инцидентом
    """
    general_values = split_multi_values(general_value)
    if not general_values or values.empty:
        return pd.Series(False, index=values.index)

    parts = values.fillna('').str.replace(',', '\n', regex=False)
    parts = parts.str.replace('\r', '\n', regex=False).str.split('\n')
    # выносим значения в отдельные строки, сохраняя индекс кандидата
    parts = parts.explode().str.strip()
    matches = parts.isin(general_values)

    # собираем результат обратно: есть совпадение — кандидат подходит
    mask = matches.groupby(level=0).any()
    return mask.reindex(values.index, fill_value=False)
