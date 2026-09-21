from django.contrib import admin
from django.conf import settings
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from filebrowser.sites import site as file_site


urlpatterns = [
    path('admin/filebrowser/', file_site.urls),
    path('grappelli/', include('grappelli.urls')),

    path('admin/', admin.site.urls),
    path('', lambda request: redirect('core:dashboard')),
    path('core/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
