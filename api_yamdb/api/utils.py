from random import randint

from django.conf import settings
from django.core.mail import send_mail


def generate_confirmation_code():
    """Генерирует код подтверждения"""
    return randint(
        settings.CONFIRMATION_CODE_MIN_VALUE,
        settings.CONFIRMATION_CODE_MAX_VALUE,
    )


def send_confirmation_code(user):
    """Отправляет код подтверждения пользователю"""
    send_mail(
        subject="Код подтверждения Yamdb",
        message=(
            "Регистрация завершена. "
            f"Ваш код подтверждения: {user.confirmation_code}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
