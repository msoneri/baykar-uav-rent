from django.urls import path
from .views import UserRegistrationView, UserLoginAPIView

app_name='api'
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login')
]
