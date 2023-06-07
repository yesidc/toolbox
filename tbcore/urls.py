from django.urls import  path
from . import views


urlpatterns = [
    path ('', views.start_page, name = 'start-page'),
    path("login/", views.ToolBoxLogingView.as_view(), name="login"),
    path('logout/', views.ToolBoxLogoutView.as_view(),name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
]