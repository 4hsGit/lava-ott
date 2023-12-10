from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class OTPSendSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(min_length=10, max_length=10)


class OTPVerfySerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10, min_length=10)
    otp = serializers.IntegerField(min_value=100000, max_value=999999,
                                   error_messages={'max_value': 'OTP must contain 6 digits.',
                                                   'min_value': 'OTP must contain 6 digits.'})
    keep_logged_in = serializers.BooleanField(default=False)


class UserRegistrationSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(max_length=10, min_length=10)
    otp = serializers.IntegerField(min_value=100000, max_value=999999,
                                   error_messages={'max_value': 'OTP must contain 6 digits.',
                                                   'min_value': 'OTP must contain 6 digits.'})

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mobile_number',
            'gender',
            'dob',
            'otp'
        )
