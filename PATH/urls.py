from django.urls import path
from . import views

app_name = 'PATH'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('/',views.home,name='home'),


]
