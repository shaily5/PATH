from django.urls import path
from . import views
from .views import homepage
from django.contrib.auth import views as auth_views
from PATH.views import ResetPasswordView

app_name = 'PATH'
urlpatterns = [
    # path('login/', views.user_login, name='login'),

    path('', homepage, name='homepage'),
    path('login/', views.LoginUser, name='login'),
    path('logout/', views.logoutView,name='logout'),
    path('register/', views.Register, name='register'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='PATH/authentication/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='PATH/authentication/password_reset_complete.html'),
         name='password_reset_complete'),

]
