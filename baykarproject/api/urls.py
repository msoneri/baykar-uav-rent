from django.urls import path
from .views import UserRegistrationView

app_name='api'
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    # Add other API endpoints as needed
]
