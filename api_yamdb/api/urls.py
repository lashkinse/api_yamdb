from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    SignUpView,
    GetTokenView,
)

router_v1 = DefaultRouter()
router_v1.register("categories", CategoryViewSet, basename="category")
router_v1.register("genres", GenreViewSet, basename="genre")
router_v1.register("titles", TitleViewSet, basename="title")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", SignUpView.as_view()),
    path("v1/auth/token/", GetTokenView.as_view()),
]
