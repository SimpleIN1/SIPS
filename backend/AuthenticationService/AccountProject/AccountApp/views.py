import orjson
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets, permissions, generics, mixins
from drf_yasg.utils import swagger_auto_schema

from AccountApp.serializers import UserModelSerializer, ResetPasswordSerializer, ResetPasswordChangeSerializer
from AccountApp.permissions import IsOwnerOrIsAdmin
from AccountApp.services.confirmation_email import confirm_email
from AccountApp.view_swagger import UserListSwagger, ResetPasswordSwagger

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


class VerifyEmailAPIView(APIView):
    def get(self, request, sessionid):
        if confirm_email(sessionid):
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect(settings.URL_FRONTEND_404)


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(responses=ResetPasswordSwagger.responses)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "An email was sent to reset the password."},
            status=HTTPStatus.OK
        )


class ResetPasswordChangeAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordChangeSerializer

    @swagger_auto_schema(responses=ResetPasswordSwagger.responses)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Successful reset the password."},
            status=HTTPStatus.OK
        )
