from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('uav-list/', views.uav_list_view, name='uav-list'),
    path('rent-uav/', views.rent_uav_view, name='rent-uav'),
    path('uav-rental-list/', views.uav_rental_list, name='uav_rental_list'),
]