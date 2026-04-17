from rest_framework.urls import path
from rest_registration.api import views
from AccountApp.views import VerifyOTPEmailRegistrationAPIView, RepeatOTPCodeEmailRegistrationAPIView, \
    VerifyOTPResetPasswordAPIView, RepeatOTPCodeResetPasswordAPIView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/verify/', views.verify_registration, name='verify-registration'),

    path('change/email/', views.register_email, name='change-email'),
    path('change/email/verify/', views.verify_email, name='verify-change-email'),
    path('change/email/otpcode/verify/', VerifyOTPEmailRegistrationAPIView.as_view(), name='verify-otpcode-email'),
    path('change/email/otpcode/repeat/', RepeatOTPCodeEmailRegistrationAPIView.as_view(), name='repeat-otpcode-email'),

    path('reset/password/', views.send_reset_password_link, name='reset-password'),
    path('reset/password/verify/', views.reset_password, name='verify-reset-password'),
    path('reset/password/otpcode/verify/', VerifyOTPResetPasswordAPIView.as_view(), name='verify-otpcode-reset-password'),
    path('reset/password/otpcode/repeat/', RepeatOTPCodeResetPasswordAPIView.as_view(), name='repeat-otpcode-reset-password'),

    path('profile/', views.profile, name='profile'),

    path('change/password/', views.change_password, name='change-password'),
]
