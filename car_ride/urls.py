from django.urls import path
from car_ride import views

app_name = 'car_ride'
urlpatterns=[
    path('',views.home, name="home"),
    path('register/', views.Register, name="register"),
    path('login/', views.LoginUser, name="login"),
    path('dashboard/', views.dash, name="dashboard"),
    path('addmycar/', views.Addcar, name="addmycar"),
    path('customerbookings/', views.CustomerBookings, name="customerbookings"),
    path('searchmycar/', views.Search, name="searchmycar"),
    path('mybookings/', views.MyBookings, name="mybookings"),
    path('myaccount', views.MyAccount,name="myaccount"),
]