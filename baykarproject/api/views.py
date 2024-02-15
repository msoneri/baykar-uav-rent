from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.core.exceptions import ValidationError
from django.core import validators

from .serializers import RegisterUserSerializer, UserLoginSerializer, UAVSerializer, UAVRentalSerializer
from app.models import UAV, UAVRental

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
            user = authenticate(request, username=User.objects.get(email=email).username, password=password)

            if user is not None:
                # login successful
                login(request, user)
                return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            # clear the session
            request.session.flush()

            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User is not authenticated."}, status=status.HTTP_400_BAD_REQUEST)


class UAVViewSet(viewsets.ModelViewSet):
    queryset = UAV.objects.all()
    serializer_class = UAVSerializer

    @permission_classes([IsAdminUser])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @permission_classes([IsAdminUser])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @permission_classes([IsAdminUser])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UAVRentalViewSet(viewsets.ModelViewSet):
    queryset = UAVRental.objects.all()
    serializer_class = UAVRentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UAVRental.objects.all()
        else:
            return UAVRental.objects.filter(renter=user)

    def perform_create(self, serializer):
        serializer.save(renter=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_staff:
            renter = serializer.validated_data.get('renter')
            if renter != request.user:
                return Response({"detail": "You do not have permission to create a rental for another user."},
                                status=status.HTTP_403_FORBIDDEN)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_staff:
            renter = serializer.validated_data.get('renter')
            if renter != request.user:
                return Response({"detail": "You do not have permission to update a rental for another user."},
                                status=status.HTTP_403_FORBIDDEN)

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_staff:
            renter = serializer.validated_data.get('renter')
            if renter != request.user:
                return Response({"detail": "You do not have permission to delete a rental for another user."},
                                status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)