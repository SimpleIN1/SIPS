from rest_framework import serializers


class VerifyOPTEmailRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(max_length=6, required=True)


class RepeatOTPCodeEmailRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerifyOPTResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(max_length=6, required=True)


class RepeatOTPCodeResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class DefaultResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=256)


class DefaultErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=256)


class VerifyOTPEmailRegistrationResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=256)
    user_id = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    timestamp = serializers.IntegerField(required=True)
    signature = serializers.CharField(required=True)


class VerifyOTPResetPasswordResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=256)
    user_id = serializers.CharField(required=True)
    timestamp = serializers.IntegerField(required=True)
    signature = serializers.CharField(required=True)


class DefaultRepeatErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=256)
    time_left = serializers.CharField(max_length=20, required=False)
