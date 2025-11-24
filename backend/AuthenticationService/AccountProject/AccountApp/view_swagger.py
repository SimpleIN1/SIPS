from drf_yasg import openapi


class UserListSwagger:
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title="UserModel",
            properties={
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, title="last_name", maxLength=150),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, title="first_name", maxLength=150),
                'middle_name': openapi.Schema(type=openapi.TYPE_STRING, title="middle_name", maxLength=150),
                'email': openapi.Schema(type=openapi.TYPE_STRING, title="email", maxLength=254),
            }
        ),
    }
