from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users import validators

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведений"""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )

    class Meta:
        model = Title
        fields = "__all__"


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений"""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""

    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "pub_date",
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    @staticmethod
    def validate_username(value):
        return validators.validate_username(value)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя"""

    username = serializers.CharField(
        required=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        validators=[
            validators.validate_username,
        ],
    )
    email = serializers.EmailField(
        required=True, max_length=settings.EMAIL_MAX_LENGTH
    )


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена"""

    username = serializers.CharField(
        required=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        validators=[
            validators.validate_username,
        ],
    )

    confirmation_code = serializers.CharField(
        required=True,
        max_length=settings.CONFIRMATION_CODE_MAX_LENGTH,
    )
