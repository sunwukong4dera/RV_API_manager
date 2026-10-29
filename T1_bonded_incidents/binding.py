import logging

logger = logging.getLogger(__name__)


def binding_rule(general: dict, second: dict, rule: dict) -> bool:
    """
    функция проверяет совпадение двух карточек по одному правилу.

    В all должны совпасть все поля, в any — хотя бы одно поле каждой группы.
    !! Между группами AND
    """
    def same(field: str) -> bool:
        value = general.get(field)
        return value not in (None, "", [], {}) and value == second.get(field)

    required: list = rule.get("all", [])
    groups: list = rule.get("any", [])

    # пустое правило
    if not required and not groups:
        return False

    if not all(
            same(field) for field in required
    ):
        return False

    for group in groups:
        if not any(
                same(field) for field in group
        ):
            return False

    return True


def binding(general_incident: dict, list_incidents: list, rule: dict) -> list[dict]:
    """
    функция возвращает карточки, совпавшие с основной по одному правилу
    """
    general_identifier = general_incident.get('identifier')

    matched_incidents = []
    seen_identifiers = {general_identifier}

    for incident in list_incidents:
        identifier = incident['identifier']

        if identifier in seen_identifiers:
            continue
        seen_identifiers.add(identifier)

        if binding_rule(general_incident, incident, rule):
            matched_incidents.append(incident)
            logger.info(f'Кандидат {identifier} для связывания к {general_identifier} '
                        f'по правилу {rule.get("name", "без названия")}')

    logger.info(f'Для основного инцидента {general_identifier} найдено кандидатов: {len(matched_incidents)}')

    return matched_incidents
