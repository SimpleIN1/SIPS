from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)


default_error_messages_serializer = {
    "no_active_account": "No active or no verify account found with the given credentials"
}


class TokenObtainPairSerializerJWT(TokenObtainPairSerializer):
    default_error_messages = default_error_messages_serializer


class TokenRefreshSerializerJWT(TokenRefreshSerializer):
    default_error_messages = default_error_messages_serializer
