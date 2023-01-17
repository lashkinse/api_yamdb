from django.db import models

from reviews.validator import validate_year


class Common(models.Model):
    """Общая модель для категорий и жанров"""

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


class Title(models.Model):
    """Модель заголовков."""

    name = models.TextField("Название", max_length=100, db_index=True)
    year = models.PositiveSmallIntegerField(
        "Год", blank=True, db_index=True, validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category,
        db_column="category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(Genre, blank=True, db_index=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель жанров и заголовков."""

    title = models.ForeignKey(
        Title, verbose_name="Произведение", on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre, verbose_name="Жанр", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title}, жанр - {self.genre}"

    class Meta:
        verbose_name = "Произведение и жанр"
        verbose_name_plural = "Произведения и жанры"
