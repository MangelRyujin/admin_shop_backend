from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import status
from rest_framework.response import Response
from apps.accounts.api.serializers.login_serializer import (
    CustomTokenObtainPairSerializer, 
    CustomTokenRefreshSerializer,
    CustomTokenVerifySerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer