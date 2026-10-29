import re
from itertools import product


def transform_rule(expression: str) -> list[dict]:
    """
    Преобразует выражение в список правил

    Между правилами списка и внутри каждой группы действует OR
    !! Между группами AND.

    Пример:
        Пример:
        externalid AND (host OR ip)
        ->
        [
            {
                'all': ['externalid'],
                'any': [
                    ['host', 'ip']
                ]
             }
        ]

    правило не должно содержать несколько групп с and соединенных or иначе
     оно распадется на несколько правил (по сути (field1 and field2) or (field3 and field4) это два независимых правила,
     проверяющих отдельные условия

    Пример:
    (field1 AND field2) OR (field3 AND field4)
    ->
    [
      {"all": ["field1", "field2"], "any": []},
      {"all": ["field3", "field4"], "any": []}
    ]


    упомяну сложное выражение где скобки могут быть не расставлены по приоритету

    Пример:
        (f1 AND f2 OR f3) AND (f4 OR f5) => ((f1 AND f2) OR f3) AND (f4 OR f5)
        ->
        [
          {
            "all": ["f1", "f2"],
            "any": [
              ["f4", "f5"]
            ]
          },
          {
            "all": ["f3"],
            "any": [
              ["f4", "f5"]
            ]
          }
        ]
    """
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError('Правило должно быть непустой строкой')

    tokens = []
    position = 0
    pattern = re.compile(r'[A-Za-z_][A-Za-z0-9_.-]*|[()]')
    while position < len(expression):
        if expression[position].isspace():
            position += 1
            continue
        match = pattern.match(expression, position)
        if match is None:
            raise ValueError(f'Недопустимый символ в позиции {position + 1}')
        token = match.group()
        if token.upper() == 'NOT':
            raise ValueError('Оператор NOT не поддерживается')
        tokens.append(token.upper() if token.upper() in ('AND', 'OR') else token)
        position = match.end()
    if len(tokens) > 256:
        raise ValueError('Правило слишком сложное (максимум 256 элементов)')

    index = 0

    def parse_atom():
        """Одно поле или выражение внутри скобок."""
        nonlocal index
        if index == len(tokens):
            raise ValueError('Ожидалось поле или открывающая скобка')
        token = tokens[index]
        index += 1
        if token == '(':
            node = parse_or()
            if index == len(tokens) or tokens[index] != ')':
                raise ValueError('Не хватает закрывающей скобки')
            index += 1
            return node
        if token in ('AND', 'OR', ')'):
            raise ValueError(f'Ожидалось поле, получено: {token}')
        return ('field', token)

    def parse_and():
        nonlocal index
        nodes = [parse_atom()]
        while index < len(tokens) and tokens[index] == 'AND':
            index += 1
            nodes.append(parse_atom())
        return nodes[0] if len(nodes) == 1 else ('and', nodes)

    def parse_or():
        nonlocal index
        nodes = [parse_and()]
        while index < len(tokens) and tokens[index] == 'OR':
            index += 1
            nodes.append(parse_and())
        return nodes[0] if len(nodes) == 1 else ('or', nodes)

    tree = parse_or()
    if index != len(tokens):
        raise ValueError(f'Лишний элемент или пропущен оператор: {tokens[index]}')

    def alternatives(node):
        """Собирает поля чистой OR-группы; AND внутри неё возвращает None."""
        kind, value = node
        if kind == 'field':
            return [value]
        if kind == 'or':
            fields = []
            for child in value:
                child_fields = alternatives(child)
                if child_fields is None:
                    return None
                fields.extend(child_fields)
            return list(dict.fromkeys(fields))
        return None

    def convert(node):
        kind, value = node
        if kind == 'field':
            return [{'all': [value], 'any': []}]
        if kind == 'or':
            fields = alternatives(node)
            if fields is not None:
                return [{'all': [], 'any': [fields]}]
            # OR между сочетаниями условий создаёт отдельные правила.
            result = []
            for child in value:
                result.extend(convert(child))
                if len(result) > 256:
                    raise ValueError('Выражение создаёт больше 256 правил')
            return result

        # AND объединяет ограничения. Если есть альтернативные правила,
        # нужны все комбинации: (A OR B) AND C -> (A AND C) OR (B AND C).
        result = [{'all': [], 'any': []}]
        for child in value:
            child_rules = convert(child)
            if len(result) * len(child_rules) > 256:
                raise ValueError('Выражение создаёт больше 256 правил')
            result = [
                {
                    'all': list(dict.fromkeys(left['all'] + right['all'])),
                    'any': left['any'] + right['any'],
                }
                for left, right in product(result, child_rules)
            ]
        return result

    return convert(tree)
