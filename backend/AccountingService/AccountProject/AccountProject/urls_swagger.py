from rest_framework import permissions

from django.conf import settings as conf
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Документации по API сервиса регистрации пользователей",
        default_version='v1',
        description="API регистрации пользователей. Cодержит следующее: регистрация, "
                    "восставновление пароля через одноразовый код, подтверждение почты по ссылке, "
                    "при измении почтового ящие подтверждение по коду, ограниченный доступ для "
                    "просмотра информации о пользователях.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="serbinovichgs@ict.nsc.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
    url=f"{conf.SCHEMA}://{conf.DOMAIN}:{conf.PORT}/{conf.MAIN_ROUTE}"
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
