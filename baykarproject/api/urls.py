from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name='api'

router = DefaultRouter()
router.register(r'uav', UAVViewSet, basename='uav')
router.register(r'uav-rental', UAVRentalViewSet, basename='uav-rental')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('', include(router.urls)),
]
