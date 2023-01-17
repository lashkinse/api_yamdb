from django.db import models


class Common(models.Model):
    """Общая модель для Category и Genre"""

    name = models.TextField(verbose_name="Наименование", max_length=100)
    slug = models.SlugField("slug", unique=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name


class Category(Common):
    """Модель категорий."""

    class Meta(Common.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(Common):
    """Модель жанров."""

    class Meta(Common.Meta):
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
