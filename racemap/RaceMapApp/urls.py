from django.urls import re_path, path

from . import views

urlpatterns = [
    path("create_map", views.create_map),
    path("maps", views.maps),
    re_path(r"^maps/(?P<map_id>[0-9]+)$", views.map_view),
    re_path(r"^maps/(?P<map_id>[0-9]+)/create_component$", views.create_component),
    re_path(r"^maps/(?P<map_id>[0-9]+)/rotate_component$", views.rotate_component),
    re_path(r"^maps/(?P<map_id>[0-9]+)/delete_component$", views.delete_component),
    path("components", views.components)
]