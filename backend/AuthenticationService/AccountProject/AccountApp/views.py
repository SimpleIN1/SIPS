from django.contrib.auth import get_user_model
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, generics, mixins
from drf_yasg.utils import swagger_auto_schema

from AccountApp.serializers import UserModelSerializer
from AccountApp.permissions import IsOwnerOrIsAdmin
from AccountApp.view_swagger import UserListSwagger


UserModel = get_user_model()


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrIsAdmin
    ]


class UserListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            # Specific permissions for GET requests
            return [
                permissions.IsAuthenticated(),
                permissions.IsAdminUser()
            ]
        # Default permissions for other methods
        return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(responses=UserListSwagger.responses)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
