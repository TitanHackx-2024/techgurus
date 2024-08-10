from django.urls import path
from . import v1_views

urlpatterns = [
    path('home/', v1_views.HomeView.as_view(), name='postify_api_home'),
    path('register_user/', v1_views.UserRegisterViewV1.as_view(), name='register_user'),
    path('login/', v1_views.login, name='login'),
    
    # content apis
    path('content/', v1_views.ContentViewV1.as_view(), name='postify_contents'),
    path('content/<int:content_id>/', v1_views.ContentViewV1.as_view(), name='postify_content'),
    
    
    # upload api
    path('content/<int:content_id>/upload/', v1_views.ContentUploadViewV1.as_view(), name='upload_content'),

    # health Check api
    path('health-check/', v1_views.HealthCheckView.as_view(), name='health-check'),
]
