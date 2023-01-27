from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username


class User(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    USER_ROLE_CHOICES = (
        (ADMIN, "admin"),
        (MODERATOR, "moderator"),
        (USER, "user"),
    )

    username = models.CharField(
        unique=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        verbose_name="Имя пользователя",
        validators=(validate_username,),
    )
    email = models.EmailField(
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH,
        verbose_name="Адрес электронной почты",
    )
    role = models.CharField(
        max_length=settings.USER_BIO_MAX_LENGTH,
        choices=USER_ROLE_CHOICES,
        default=USER,
        verbose_name="Роль пользователя",
    )
    bio = models.TextField(
        max_length=settings.USER_BIO_MAX_LENGTH,
        blank=True,
        verbose_name="Биография пользователя",
    )
    confirmation_code = models.CharField(
        max_length=settings.CONFIRMATION_CODE_MAX_LENGTH,
        blank=True,
        verbose_name="Код доступа",
    )

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
