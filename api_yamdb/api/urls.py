from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from api.v1.urls import urlpatterns as v1_urls

urlpatterns = [
    path("v1/", include(v1_urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "doc/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
