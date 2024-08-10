from django.urls import path
from . import v1_views

urlpatterns = [
    path('home/', v1_views.HomeView.as_view(), name='postify_api_home'),
]
