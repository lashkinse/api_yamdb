from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from reviews.validator import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель категорий."""

    name = models.TextField(
        verbose_name="Наименование категории", max_length=256
    )
    slug = models.SlugField("slug", max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    """Модель жанров."""

    name = models.TextField(verbose_name="Наименование жанра", max_length=256)
    slug = models.SlugField("slug", max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    """Модель заголовков."""

    name = models.TextField("Название", max_length=256, db_index=True)
    year = models.PositiveSmallIntegerField(
        "Год", blank=True, db_index=True, validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(Genre, blank=True, db_index=True)
    description = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class GenreTitle(models.Model):
    """Модель жанров и произведений."""

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


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("-pub_date",)
        constraints = (
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_pair"
            ),
        )


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        verbose_name="Отзыв",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)
