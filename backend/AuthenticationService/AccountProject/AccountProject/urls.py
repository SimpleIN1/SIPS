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


# Project route
MAIN_ROUTE = "api/account"
AUTH_ROUTE = f"{MAIN_ROUTE}/auth"


urlpatterns = [
    path(f'admin/', admin.site.urls),
    path(f'{MAIN_ROUTE}/', include("AccountApp.urls")),
    path(f'{MAIN_ROUTE}/swagger/', include("AccountProject.urls_swagger")),
    path(f'{AUTH_ROUTE}/', include("AuthApp.urls")),
]

