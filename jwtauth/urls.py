from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import registration, MyTokenObtainPairView

urlpatterns = [
    path("register/", registration, name="register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
