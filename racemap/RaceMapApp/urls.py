from django.urls import re_path, path

from . import views

urlpatterns = [
    path("create_map", views.create_map)
]