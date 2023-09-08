from django.urls import  path
from . import views
from django.contrib.auth import views as auth_views

# TODO need a place to put the link to the password change page

urlpatterns = [
    path ('', views.start_page, name = 'start-page'),
    path("login/", views.ToolBoxLogingView.as_view(), name="login"),
    path('logout/', views.ToolBoxLogoutView.as_view(),name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.ActivateAccountView.as_view(), name='activate'),
    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/change_password.html',
            success_url='/'
        ),
        name='change_password'
    ),

    # Forget Password
    path('password-reset/',
         views.ToolBoxResetPasswordView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),


]