from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_number(value):
    if not str(value).isdigit():
        raise ValidationError(
            f"Значение {value} не является числом",
        )
    return value


def validate_year(value):
    validate_number(value)
    if value > timezone.now().year:
        raise ValidationError("Год выпуска больше текущего")
    if value < 1900:
        raise ValidationError("Год выпуска меньше 1900")
    return value
