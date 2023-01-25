from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdminOrReadOnly, IsAdmin
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    SignUpSerializer,
    GetTokenSerializer,
    UserSerializer,
)
from api.utils import send_confirmation_code, generate_confirmation_code
from reviews.models import Category, Genre, Title

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


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
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            is_user_exists = User.objects.filter(username=username).exists()
            is_email_exists = User.objects.filter(email=email).exists()
            if not (is_user_exists and is_email_exists):
                if is_user_exists:
                    return Response(
                        {
                            "detail": "Пользователь с таким именем уже существует"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if is_email_exists:
                    return Response(
                        {
                            "detail": "Пользователь с таким email уже существует"
                        },
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
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
