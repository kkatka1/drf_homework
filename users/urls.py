from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("list/", UserListAPIView.as_view(), name="user-list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("<int:pk>/update", UserUpdateAPIView.as_view(), name="users_update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="users_delete"),

    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh")
]
