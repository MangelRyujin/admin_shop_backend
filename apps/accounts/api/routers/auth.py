from dj_rest_auth.views import LogoutView, PasswordChangeView,UserDetailsView
from django.urls import path
from apps.accounts.api.views.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView
from apps.accounts.api.views.user_views import UserListView

urlpatterns = [
    
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("user/profile/",UserDetailsView.as_view(),name="user_datail"),
    path('user/all', UserListView.as_view(), name='user-list'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
]
