from django.contrib.auth.models import AbstractUser
from django.db import models


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
        max_length=30,
        verbose_name="Имя пользователя",
    )
    email = models.EmailField(
        unique=True,
        max_length=100,
        verbose_name="Адрес электронной почты",
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLE_CHOICES,
        default=USER,
        verbose_name="Роль пользователя",
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография пользователя",
    )

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR
