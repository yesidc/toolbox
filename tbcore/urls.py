from django.contrib import admin
from django.urls import include, path, re_path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path ('', views.start_page, name = 'start-page'),
    path("login/", views.ToolBoxLogingView.as_view(), name="login"),
    path('logout/', views.ToolBoxLogoutView.as_view(),name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]