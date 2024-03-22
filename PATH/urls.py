from django.urls import path
from . import views
from .views import homepage


app_name = 'PATH'
urlpatterns = [
    # path('login/', views.user_login, name='login'),

    path('', homepage, name='homepage'),
    path('login/', views.LoginUser, name='login'),
    path('register/', views.Register, name='register'),
    path('logout/', views.logoutView,name='logout')

]
