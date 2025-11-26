
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.sessions.backends.cache import SessionStore # cache
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)

from AccountApp.services.confirmation_email import send_confirmation_email, send_reset_password_email, \
    confirm_reset_password_email

UserModel = get_user_model()


class PasswordValidateSerializer:
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return value


class UserModelSerializer(PasswordValidateSerializer, serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ["last_name", "first_name", "middle_name", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data['password']
        del validated_data['password']

        user = UserModel(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()

        send_confirmation_email(user)

        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("User not found")

        return value

    def save(self):
        send_reset_password_email(self.user)


class ResetPasswordChangeSerializer(PasswordValidateSerializer, serializers.Serializer):
    password = serializers.CharField(max_length=250)
    sessionid = serializers.CharField(max_length=100)

    def save(self):
        user_id = confirm_reset_password_email(self.validated_data["sessionid"])
        if not user_id:
            raise serializers.ValidationError({"sessionid": ["Invalid field"]})

        print("password", self.validated_data["password"])
        secure_password = make_password(self.validated_data["password"])
        UserModel.objects.filter(id=user_id).update(password=secure_password)


default_error_messages_serializer = {
    "no_active_account": "No active or no verify account found with the given credentials"
}


class TokenObtainPairSerializerJWT(TokenObtainPairSerializer):
    default_error_messages = default_error_messages_serializer


class TokenRefreshSerializerJWT(TokenRefreshSerializer):
    default_error_messages = default_error_messages_serializer
