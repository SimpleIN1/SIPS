from rest_framework import routers, urls

from AccountApp import views

# router = routers.SimpleRouter()
# # router.register(r"users", views.UserCreateModelViewSet, basename="user-create")
# router.register(r"users", views.UserListModelViewSet, basename="user-list")


urlpatterns = [
    # urls.path("users/", views.UserCreateAPIView.as_view(), name="user-create"),
    # urls.path("users/", views.UserListAPIView.as_view(), name="user-list"),
    urls.path("users/", views.UserListCreateAPIView.as_view(), name="user-list-create"),
    urls.path("users/<int:pk>/", views.UserRetrieveUpdateDestroyAPIView.as_view(), name="user-rud")
]
# urlpatterns += router.urls