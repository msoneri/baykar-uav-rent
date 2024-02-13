from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.core.exceptions import ValidationError
from django.core import validators

from .serializers import RegisterUserSerializer, UserLoginSerializer

# Register user API view
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not User.objects.filter(email=serializer.validated_data['email'].lower()).exists():
                serializer.save()
                return Response({'message': serializer.data['email']}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'This email address is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        else:    
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # authenticate user
            user = authenticate(request, username=email, password=password)


            if user is not None:
                # login successful
                login(request, user)
                return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        