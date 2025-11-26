from rest_framework import routers, urls

from AccountApp import views


urlpatterns = [
    urls.path("users/", views.UserListCreateAPIView.as_view(), name="user-list-create"),
    urls.path("users/<int:pk>/", views.UserRetrieveUpdateDestroyAPIView.as_view(), name="user-rud"),
    urls.path("verify/<str:sessionid>/", views.VerifyEmailAPIView.as_view(), name="email-verify"),
    urls.path("resetpassword/", views.ResetPasswordAPIView.as_view(), name="rest-password"),
    urls.path("resetpassword/change/", views.ResetPasswordChangeAPIView.as_view(), name="rest-password-change"),
]
