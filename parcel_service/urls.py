from django.urls import path
from . import views
app_name='parcel_service'
urlpatterns = [

    path('homepage/', views.homepage, name='homepage'),
    path('', views.parcel_list, name='parcel_list'),
    path('parcel/<int:parcel_id>/', views.parcel_detail, name='parcel_detail'),
    path('parcel/new/', views.create_parcel, name='create_parcel'),
    path('parcel/new/<int:ride_id>/', views.create_parcel, name='create_parcel'),

path('dashboard/parcel_request/<int:ride_id>/', views.parcel_requests_view, name='parcel_request'),
    path('create_parcel_ride/', views.create_parcel_ride, name='create_parcel_ride'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_enduser/', views.dashboard_enduser, name='dashboard_enduser'),
    path('get_ride_details/<int:ride_id>/', views.get_ride_details, name='get_ride_details'),
    path('submit_parcel_request/<int:ride_id>/', views.submit_parcel_request, name='submit_parcel_request'),
    path('get_parcel_requests/<int:ride_id>/', views.get_parcel_requests, name='get_parcel_request'),
]
