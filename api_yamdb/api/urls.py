from django.urls import include, path

from api.v1.urls import urlpatterns as v1_urls

urlpatterns = [
    path("v1/", include(v1_urls)),
]
