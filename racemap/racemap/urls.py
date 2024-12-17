"""
URL configuration for racemap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from RaceMapApp.views import index, register, login_view, logout_view
from RaceMapApp.models import Map, ComponentRegistry, Component, Car
from classes.server import Server
from multiprocessing import Process

urlpatterns = [
    path("", index),
    path('admin/', admin.site.urls),
    path("accounts/login/", login_view),
    path("accounts/logout/", logout_view),
    path("accounts/register/", register),
    path('accounts/', include('django.contrib.auth.urls')),
    path("racemap/", include("RaceMapApp.urls"))
]

s = Server("127.0.0.1", 8001)
p = Process(target=s.start_server)
p.start()

Map.objects.all().delete()
for c in ComponentRegistry.objects.all():
    c.is_registered = False
    c.save()
Component.objects.all().delete()
Car.objects.all().delete()