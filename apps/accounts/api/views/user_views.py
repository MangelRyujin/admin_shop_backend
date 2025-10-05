from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from apps.accounts.api.serializers.change_password_serializer import ChangePasswordSerializer
from apps.accounts.api.serializers.user_serializer import UserRegisterSerializer, UserSerializer, UserUpdateSerializer, UserUpdateStatusSerializer
from apps.accounts.models import User
from utils.permission.admin import IsAdminGroup
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class UserPagination(PageNumberPagination):
    """
    Custom pagination configuration
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserListView(generics.ListAPIView):
    """
    View to list all users
    Requires authentication and admin role
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminGroup]
    pagination_class = UserPagination

    def get_queryset(self):
        """
        Customize the queryset with ordering by email
        """
        queryset = User.objects.all()
        queryset = queryset.order_by('id')
        return queryset

class UserRegisterAPIView(APIView):
    permission_classes = (IsAuthenticated,IsAdminGroup)
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'data': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserIdChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,IsAdminGroup)
    
    def put(self, request, pk):
        user = get_object_or_404(User,pk=pk)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password_1'])
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,IsAdminGroup)
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return User.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"data": response.data}, status=status.HTTP_200_OK)

class UserToggleStatusAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsAdminGroup)
    queryset = User.objects.all()
    serializer_class = UserUpdateStatusSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return Response({"data": UserSerializer(user).data}, status=status.HTTP_200_OK)
   
class UserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,IsAdminGroup)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)