from datetime import date, datetime
from typing import Union


def check_type_value_party(value_party: str) -> Union[str, int, None, bool, date, datetime]:
    """Проверка значение на его тип"""
    value_party = value_party.strip()

    if value_party.lower() == "true":
        return True

    if value_party.lower() == "false":
        return False

    type_conversions = {
        int: int,
        date: lambda value: datetime.strptime(value, "%Y-%m-%d").date(),
        datetime: lambda value: datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f %z"),
        str: str
    }

    for _, conversions_func in type_conversions.items():
        try:
            return conversions_func(value_party)
        except (ValueError, TypeError):
            pass  # Значение не может быть преобразовано в тип

    return None
