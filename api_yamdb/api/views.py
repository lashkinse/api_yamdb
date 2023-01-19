from django.db.models import Avg
from rest_framework import viewsets

from api.permissions import IsAdminOrReadOnly
from api.serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('review__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    filterset_fields = ['name']
    ordering_fields = ('name',)
