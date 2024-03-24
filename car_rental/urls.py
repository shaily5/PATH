from django.template.context_processors import static
from django.urls import path, include

from PATH_project import settings
from car_rental import views
from django.contrib.auth import views as auth_views
from car_rental.views import ResetPasswordView


urlpatterns = [
    path('cars/', views.car_list, name='car-list'),
    path('rental_reservation_list/', views.rental_reservation_list, name='rental_reservation_list'),
    path('invoice/<str:invoice_number>/', views.rental_invoice_detail, name='rental_invoice_detail'),
    path('rental/dashboard/', views.homepage, name='dashboard'),
    path('create_new_car/', views.create_car, name='create_car'),


    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('car_rental/login/', views.loginView, name='rentallogin'),
    path('car_rental/signup/', views.signup, name='signup'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='car_rental/authentication/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='car_rental/authentication/password_reset_complete.html'),
         name='password_reset_complete'),

    path('car_rental/bookaCar/',views.bookRentalCar,name='bookRentalCar'),
    path('car_rental/getCars/<str:param>/', views.getCars, name='getCars'),

    path('car_rental/getCarDetail/<int:car_id>/', views.getCarDetail, name='getCarDetail'),

    path('car_rental/addLicenseDetails/<int:car_id>/<str:car_type>', views.license_detail_view, name='license_detail_view'),

    path('car_rental/getReservations', views.getReservations,
         name='getReservations'),
    path('car_rental/userDashboard', views.showUserDashboard,
         name='userDashboard'),


]

