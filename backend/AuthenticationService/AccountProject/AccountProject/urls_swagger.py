from rest_framework import permissions
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Документации по API миксросервиса аутентификации пользователей",
      default_version='v1',
      description="API аутентификации пользователей содержит следующее: регистарация, автризация, просмотр личной информации, восставновление, ограниченный доступ для просмотра файов о пользователях.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="serbinovichgs@ict.nsc.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
