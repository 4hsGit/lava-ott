from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class OTPSendSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10)


class OTPVerfySerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10)
    otp = serializers.CharField(min_length=6, max_length=6)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mobile_number',
            'gender',
            'dob',
        )
