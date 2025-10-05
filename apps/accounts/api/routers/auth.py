from dj_rest_auth.views import LogoutView, PasswordChangeView,UserDetailsView
from django.urls import path
from apps.accounts.api.views.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView
from apps.accounts.api.views.user_views import UserIdChangePasswordView, UserToggleStatusAPIView, UserListView, UserRegisterAPIView, UserUpdateAPIView, UserDeleteAPIView

urlpatterns = [
    
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("user/profile/",UserDetailsView.as_view(),name="user_datail"),
    path('user/all', UserListView.as_view(), name='user-list'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path("user/register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("user/<int:pk>/change-status/", UserToggleStatusAPIView.as_view(), name="user-change-status-by-id"),
    path("user/<int:pk>/change-password/", UserIdChangePasswordView.as_view(), name="user-change-password-by-id"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update-by-id"),
    path("user/<int:pk>/delete/", UserDeleteAPIView.as_view(), name="user-delete-by-id"),
]
