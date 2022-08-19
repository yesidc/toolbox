from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path ('', views.start_page, name = 'start-page'),
    path("accounts/", include("django.contrib.auth.urls")),
]