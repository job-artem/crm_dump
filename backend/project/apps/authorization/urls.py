from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    LoginUserAPI, RegistrationUserAPI, ConfirmAPI,
    UserDataApi, ImageAPI, TimeGetAPI
)

urlpatterns = [
    path('registration/', RegistrationUserAPI.as_view()),
    path('login/', LoginUserAPI.as_view()),
    path('confirm/', ConfirmAPI.as_view()),
    path('get_token/', TokenObtainPairView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
    path('user/profile/', UserDataApi.as_view()),
    path('user/image/', ImageAPI.as_view()),
    path('user/time/', TimeGetAPI.as_view()),
]
