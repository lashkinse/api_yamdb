from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    SignUpSerializer,
    GetTokenSerializer,
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


class GetTokenView(ObtainAuthToken):
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


class SignUpView(ObtainAuthToken):
    """Регистрация пользователя"""

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data, many=False)
        if serializer.is_valid():
            user = serializer.save()
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
