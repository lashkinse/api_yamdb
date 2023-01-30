from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.mixins import CustomMixin
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsStaffOrAuthorOrReadonly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTokenSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             UserSerializer)
from api.utils import generate_confirmation_code, send_confirmation_code
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategoryViewSet(CustomMixin):
    """Категории"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CustomMixin):
    """Жанры"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения"""

    queryset = (
        Title.objects.all()
        .annotate(rating=Avg("reviews__score"))
        .order_by("-id")
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitleWriteSerializer
        return TitleReadSerializer


class GetTokenView(views.APIView):
    """Получение токена для авторизации пользователя"""

    def post(self, request, *args, **kwargs):
        serializer = GetTokenSerializer(data=request.data, many=False)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            confirmation_code = serializer.validated_data["confirmation_code"]
            user = get_object_or_404(User, username=username)
            if user.confirmation_code != confirmation_code:
                return Response(
                    {"detail": "Неверный код доступа"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"token": str(RefreshToken.for_user(user).access_token)}
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class SignUpView(views.APIView):
    """Регистрация пользователя"""

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data, many=False)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        is_user_exists = User.objects.filter(username=username).exists()
        is_email_exists = User.objects.filter(email=email).exists()
        if not (is_user_exists and is_email_exists):
            if is_user_exists:
                return Response(
                    {"detail": "Пользователь с таким именем уже существует"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if is_email_exists:
                return Response(
                    {"detail": "Пользователь с таким email уже существует"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        user, created = User.objects.get_or_create(
            username=username, email=email
        )
        user.confirmation_code = generate_confirmation_code()
        user.save()
        send_confirmation_code(user)
        return Response(
            {
                "email": user.email,
                "username": user.username,
            }
        )


class UserViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    lookup_field = "username"
    search_fields = [
        "=username",
    ]
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        methods=("get", "patch"),
        detail=False,
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def my_account(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        if not (serializer.is_valid()):
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == "GET":
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.validated_data["role"] = request.user.role
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsStaffOrAuthorOrReadonly,
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        if title.reviews.filter(author=self.request.user).exists():
            raise ValidationError("Вы уже оставили отзыв")
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsStaffOrAuthorOrReadonly,
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
