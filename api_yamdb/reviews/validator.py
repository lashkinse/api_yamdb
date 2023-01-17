import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    if not value.isdigit():
        raise ValidationError(
            f"Значение {value} не является числом",
        )
    if value > dt.date.today().year:
        raise ValidationError("Год выпуска больше текущего")
    return value
