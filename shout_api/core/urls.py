from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from core.views.users import UserRegistrationView, UserDetailView, CustomTokenObtainPairView, RolesView

from core.views.contents import ContentViewSet

content_router = DefaultRouter()
content_router.register(r'contents', ContentViewSet)



urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='register'),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users', UserDetailView.as_view(), name='user_detail'),

    # Content API
    path('', include(content_router.urls)),
    
    # Roles
    path('roles/', RolesView.as_view(), name='roles'),
]