from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)


default_error_messages_serializer = {
    "no_active_account": "No active or no verify account found with the given credentials"
}


class TokenAppendField:
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class TokenObtainPairSerializerJWT(TokenAppendField, TokenObtainPairSerializer):
    default_error_messages = default_error_messages_serializer


class TokenRefreshSerializerJWT(TokenAppendField, TokenRefreshSerializer):
    default_error_messages = default_error_messages_serializer
