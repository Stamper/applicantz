from django.urls import path

from main.api import api

urlpatterns = [
    path("api/", api.urls),
]
