"""AccountProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from rest_framework.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

# Project route
MAIN_ROUTE = "api/account"
AUTH_ROUTE = f"{MAIN_ROUTE}/auth"


urlpatterns = [
    path(f'admin/', admin.site.urls),
    path(f'{MAIN_ROUTE}/', include("AccountApp.urls")),
    path(f'{MAIN_ROUTE}/', include("AccountProject.urls_swagger")),

    path(f'{AUTH_ROUTE}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{AUTH_ROUTE}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(f'{AUTH_ROUTE}/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

