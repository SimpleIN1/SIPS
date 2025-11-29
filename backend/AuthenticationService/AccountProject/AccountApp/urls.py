from rest_framework.urls import path
from rest_registration.api import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/verify/', views.verify_registration, name='verify-registration'),

    path(
        'reset-password/send-link/', views.send_reset_password_link,
        name='send-reset-password-link',
    ),
    path('reset-password/', views.reset_password, name='reset-password'),

    path('profile/', views.profile, name='profile'),

    path('change-password/', views.change_password, name='change-password'),

    path('register-email/', views.register_email, name='register-email'),
    path('register-email/verify/', views.verify_email, name='verify-email'),
]
