from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class UserRegistrationView(generics.CreateAPIView):
    model = User

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password)
        return Response({'email': user.email}, status=status.HTTP_201_CREATED)
