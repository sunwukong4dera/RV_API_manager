from config import EXTEND_FILTERS_PATH
from util import get_extend_filter


def extend_filter_for_applicants(
        filters_for_applicants: list
) -> list:
    """
    функция дополняет фильтр, прибавляя условия, соответствующие уникальному ключу правила на контракте
        <компания.правило>

    пример:
        для контракта с ID: 1 и правилом: "AB-CD-01" ключ будет иметь вид:
        "1.AB-CD-01": [
            {
                "rule": "NEW RULE",
                ...
            }
        ]

    :param filters_for_applicants:
    :return:
    """
    company = next(
        (f["value"] for f in filters_for_applicants if f["property"] == "company")
        , None
    )
    externalid = next(
        (f["value"] for f in filters_for_applicants if f["property"] == "externalid")
        , None
    )

    extend_filter: list | None = get_extend_filter(EXTEND_FILTERS_PATH, company, externalid)

    current_filter = filters_for_applicants.copy()
    if extend_filter is not None:
        current_filter.extend(extend_filter)

    return current_filter
