import datetime as dt

from django.core.exceptions import ValidationError


def validate_number(value):
    if not str(value).isdigit():
        raise ValidationError(
            f"Значение {value} не является числом",
        )
    return value


def validate_year(value):
    validate_number(value)
    if value > dt.date.today().year:
        raise ValidationError("Год выпуска больше текущего")
    return value


def validate_score(value):
    validate_number(value)
    if value < 1 or value > 10:
        raise ValidationError(
            f"Значение {value} должно быть в диапазоне от 1 до 10",
        )
    return value
