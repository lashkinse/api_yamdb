from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений"""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


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

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        pass
