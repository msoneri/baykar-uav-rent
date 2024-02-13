from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email'].lower()
        user = User(
            email=email,
            username=email,
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

        user = authenticate(request=self.context.get('request'), username=email, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        data['user'] = user
        return data