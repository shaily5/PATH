from django.urls import path
from . import views

urlpatterns = [
    # path('register_driver/', views.register_driver, name='register_driver'),
    # path('login_driver/', views.login_driver, name='login_driver'),
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('post_ride/', views.post_ride, name='post_ride'),
    path('all_rides/', views.all_rides, name='all_rides'),
    path('about_us/', views.about_us, name='about_us'),
    #path('contact_us/', views.contact_us, name='contact_us'),
    path('edit_ride/<int:ride_id>/', views.edit_ride, name='edit_ride'),
    path('passenger_home/', views.passenger_home, name='passenger_home'),
    path('passenger_rides/', views.passenger_rides, name='passenger_rides'),
    # path('book_ride/<int:ride_id>/', views.book_ride, name='book_ride'),
    path('passenger_confirm/', views.passenger_confirm, name='passenger_confirm'),
    path('all_booked_rides/', views.all_booked_rides, name='all_booked_rides'),

]
