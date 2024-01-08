from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class OTPSendSerializer(serializers.Serializer):
    mobile_number = serializers.IntegerField(min_value=1000000000, max_value=9999999999)


class OTPVerfySerializer(serializers.Serializer):
    mobile_number = serializers.IntegerField(min_value=1000000000, max_value=9999999999)
    otp = serializers.IntegerField(min_value=100000, max_value=999999,
                                   error_messages={'max_value': 'OTP must contain 6 digits.',
                                                   'min_value': 'OTP must contain 6 digits.'})
    keep_me_logged_in = serializers.BooleanField(default=False)


class RegistrationOTPVerfySerializer(serializers.Serializer):
    mobile_number = serializers.IntegerField(min_value=1000000000, max_value=9999999999)
    otp = serializers.IntegerField(min_value=100000, max_value=999999,
                                   error_messages={'max_value': 'OTP must contain 6 digits.',
                                                   'min_value': 'OTP must contain 6 digits.'})


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    mobile_number = serializers.IntegerField(min_value=1000000000, max_value=9999999999)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mobile_number',
            'gender',
            'dob',
        )
