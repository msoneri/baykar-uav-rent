from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from app.models import UAV, UAVRental


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email'].lower()
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        user = User(
            email=email,
            username=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate(self, data):
         # here data has all the fields which have validated values
         # so we can create a User instance out of it
         user = User(**data)
         
         # get the password from the data
         password = data.get('password')
         
         errors = dict() 
         try:
             # validate the password and catch the exception
             validators.validate_password(password=password, user=user)
         
         # the exception raised here is different than serializers.ValidationError
         except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)
         
         if errors:
             raise serializers.ValidationError(errors)
          
         return super(RegisterUserSerializer, self).validate(data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')

        try:
            user = authenticate(request=self.context.get('request'), username=User.objects.get(email=email).username, password=password)
        except:
            raise serializers.ValidationError('Invalid email or password.')

        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UAVSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = UAV
        fields = ['id', 'brand', 'model', 'category', 'weight']
        datatables_always_serialize = ('id')


class UAVRentalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UAVRental
        fields = ['id', 'renter', 'uav', 'user_info', 'user_email', 'uav_info', 'rent_start_date', 'rent_end_date']
        datatables_always_serialize = ('id')