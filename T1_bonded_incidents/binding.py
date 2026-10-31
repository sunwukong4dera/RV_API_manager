import logging

from incidents import get_incidents_list
from util import match_company_id, get_incident_results
from actives import get_binding_rules
from .got_incident import explore_incident
from .transform_rule import transform_rule

logger = logging.getLogger(__name__)


def binding_rule(general: dict, second: dict, rule: dict) -> bool:
    """
    функция проверяет совпадение двух карточек по одному правилу.

    В all должны совпасть все поля, в any — хотя бы одно поле каждой группы.
    !! Между группами AND
    """
    def same(field: str) -> bool:
        value = general.get(field)
        logger.info(f'=== поле {field} основного ({general.get("identifier")}): {general.get(field)},'
                    f' поле второго ({second.get("identifier")}): {second.get(field)}')
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


def get_applicants_with_rule(general_incident: dict, list_incidents: list, rule: dict, rule_name: str='без названия') -> list[dict]:
    """
    функция возвращает карточки, совпавшие с основной по одному правилу
    """
    general_identifier = general_incident.get('identifier')

    matched_incidents = []
    seen_identifiers = {general_identifier}

    logger.info(f'== Првоерка по условию заупщена... ')
    for incident in list_incidents:
        identifier = incident['identifier']

        if identifier in seen_identifiers:
            continue
        seen_identifiers.add(identifier)

        if binding_rule(general_incident, incident, rule):
            matched_incidents.append(incident)
            logger.info(f'Кандидат {identifier} для связывания к {general_identifier} '
                        f'по правилу {rule_name}')

    logger.info(f'Для основного инцидента {general_identifier} найдено кандидатов: {len(matched_incidents)}')

    return matched_incidents


def binding(identifier: str):
    filter_incident = [
                        {
                            "property": "identifier",
                            "operator": "=",
                            "value": identifier
                        }
                    ]
    current_incident: dict | None = next(
            (inc for inc in get_incident_results(
                get_incidents_list(
                    limit=1,
                    filter=filter_incident
                )
            ) if inc['identifier'] == identifier
        ),
        None
    )

    if not current_incident:
        raise ValueError("ошибка binding: Инцидент не найден")

    company_id, applicants_list = explore_incident(current_incident)

    company_name: str | None = match_company_id(company_id)
    if not company_name:
        raise ValueError("ошибка binding: Компания не найдена")
    logger.info(f'== ID компании {company_id} преобразован в название: {company_name}')

    filter_company = [
        {
            "property": "field_binding_rules_org",
            "operator": "=",
            "value": company_name
        }
    ]
    binding_rules_fields = ["name", "field_binding_rules_org", "field_binding_rules_condition"]
    rules = get_binding_rules(
        limit=10,
        filter=filter_company,
        fields=binding_rules_fields
    )
    rules_list: list | None = rules.get("data")
    if not rules_list:
        logger.info(f'=== кандидатов нет! ===')
        return

    for rule in rules_list:
        expression, rule_name = rule.get("field_binding_rules_condition"), rule.get("name")
        logger.info(f'== Условие: {expression}')
        real_rules: list = transform_rule(expression)
        logger.info(f'== Готовое правило: {real_rules}')
        for real_rule in real_rules:
            applicants = get_applicants_with_rule(current_incident, applicants_list, real_rule, rule_name=rule_name)
            applicants_identifiers: list = [a["identifier"] for a in applicants]
            if applicants_identifiers:
                logger.info(f'=== найденные кандидаты по правилу "{rule_name}": {", ".join(applicants_identifiers)} ===')
