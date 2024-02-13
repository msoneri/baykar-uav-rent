from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'app'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    # path('', views.index, name='index'),
    # path('add_sale/', views.add_sale, name='add_sale'),
    # path('sale_history/', views.sale_history, name='sale_history'),
    # path('charts/', views.charts, name='charts'),
]