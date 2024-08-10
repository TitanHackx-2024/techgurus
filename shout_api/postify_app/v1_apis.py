from django.urls import path
from . import v1_views

urlpatterns = [
    path('home/', v1_views.HomeView.as_view(), name='postify_api_home'),
    path('register_user/', v1_views.UserRegisterViewV1.as_view(), name='register_user'),
    path('login/', v1_views.login, name='login'),
]
