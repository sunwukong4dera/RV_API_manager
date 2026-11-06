"""Применение правил к колонкам DataFrame, без обхода карточек по строкам."""
import logging
from itertools import groupby

import pandas as pd

from .transform_rule import transform_rule
from .multi_values import has_multi_values, multi_value_mask

logger = logging.getLogger(__name__)


def rule_mask(general_incident: dict, frame: pd.DataFrame, rule: dict) -> pd.Series:
    def same(field):
        value = general_incident.get(field)
        if field not in frame or value is None or isinstance(value, (list, dict)) and not value:
            return pd.Series(False, index=frame.index)
        if isinstance(value, str) and value == '':
            return pd.Series(False, index=frame.index)
        if isinstance(value, (list, dict)):
            raise ValueError(f'Поле {field}: сравнение объектов и списков масками пока не поддерживается')
        if pd.isna(value):
            return pd.Series(False, index=frame.index)
        if has_multi_values(field, value, frame[field]):
            mask = multi_value_mask(value, frame[field])
        else:
            mask = frame[field].notna() & frame[field].eq(value).fillna(False)
        logger.info(f'=== поле {field} основного ({general_incident.get("identifier")}): {value}; '
                    f'совпадений: {int(mask.sum())}')
        return mask

    required, groups = rule.get('all', []), rule.get('any', [])
    mask = pd.Series(bool(required or groups), index=frame.index)
    for field in required:
        mask &= same(field)
    for group in groups:
        group_mask = pd.Series(False, index=frame.index)
        for field in group:
            group_mask |= same(field)
        mask &= group_mask
    return mask


def apply_frame_rules(general_incident: dict, frame: pd.DataFrame, rules: list,
                      priority_field: str | None = None) -> pd.DataFrame:
    """Возвращает совпадения первого сработавшего приоритета в порядке frame.

    Меньшее число приоритета важнее. Правила одного приоритета объединяются.
    Без priority_field все правила считаются равноприоритетными.
    Компания, возраст и критичность подготовлены до вызова этой функции.
    """
    if frame.empty:
        logger.info(f'Итоговый DataFrame кандидатов:\n{frame.to_string(index=False)}')
        return frame.copy()
    frame = frame.loc[frame['identifier'].ne(general_incident['identifier'])].drop_duplicates('identifier')
    ordered = [(int(rule[priority_field]) if priority_field else 1, rule) for rule in rules]
    ordered.sort(key=lambda item: item[0])
    if not priority_field:
        logger.info('Тег приоритета не задан: все правила обрабатываются с одинаковым приоритетом.')

    for priority, entries in groupby(ordered, key=lambda item: item[0]):
        combined = pd.Series(False, index=frame.index)
        names = pd.Series('', index=frame.index)
        for _, rule in entries:
            expression, rule_name = rule.get('field_binding_rules_condition'), rule.get('name')
            logger.info(f'== Условие: {expression}')
            try:
                real_rules = transform_rule(expression)
                logger.info(f'== Готовое правило: {real_rules}')
                logger.info('== Првоерка по условию заупщена... ')
                mask = pd.Series(False, index=frame.index)
                for real_rule in real_rules:
                    mask |= rule_mask(general_incident, frame, real_rule)
            except ValueError as error:
                logger.error(f'Ошибка в правиле "{rule_name}": {error}. Правило пропущено!!!')
                continue
            combined |= mask
            names.loc[mask] = names.loc[mask] + str(rule_name) + '; '
            identifiers = frame.loc[mask, 'identifier'].tolist()
            logger.info(f'Для основного инцидента {general_incident["identifier"]} найдено кандидатов: {len(identifiers)}')
            if identifiers:
                logger.info(f'=== найденные кандидаты по правилу "{rule_name}": {", ".join(identifiers)} ===')

        if combined.any():
            result = frame.loc[combined].copy()
            result['rule_priority'] = priority
            result['matched_rules'] = names.loc[combined].str.rstrip('; ')
            break
    else:
        result = frame.iloc[:0].copy()

    # показываем компактную таблицу без сотен технических полей карточки.
    columns = [c for c in ('identifier', 'incident_uuid', 'level', 'severity_rank',
                           'creation', 'rule_priority', 'matched_rules') if c in result]
    logger.info(f'Итоговый DataFrame кандидатов:\n{result[columns].to_string(index=False)}')
    return result
