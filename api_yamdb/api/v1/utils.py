import uuid

from django.conf import settings
from django.core.mail import send_mail


def generate_confirmation_code():
    """Генерирует код подтверждения"""
    return uuid.uuid4()


def send_confirmation_code(user):
    """Отправляет код подтверждения пользователю"""
    send_mail(
        subject="Код подтверждения Yamdb",
        message=(
            "Регистрация завершена. "
            f"Ваш код доступа: {user.confirmation_code}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
