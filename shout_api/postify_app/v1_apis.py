from django.urls import path
from . import v1_views

urlpatterns = [
    path('home/', v1_views.HomeView.as_view(), name='postify_api_home'),
    
    # user apis
    path('register_user/', v1_views.UserRegisterViewV1.as_view(), name='register_user'),
    path('login/', v1_views.login, name='login'),
    path('user/<int:user_id>/', v1_views.UserDetailViewV1.as_view(), name='get_postify_user'),
    
    # account apis
    path('account/<int:account_id>/users', v1_views.AccountUsersViewV1.as_view(), name='account_users'),
    
    # content apis
    path('content/', v1_views.ContentViewV1.as_view(), name='postify_contents'),
    path('content/<int:content_id>/', v1_views.ContentViewV1.as_view(), name='postify_content'),
    
    
    # roles apis
    path('account_roles/', v1_views.AccountRolesViewV1.as_view(), name='account_roles'),
    
    
    # upload api
    path('content/<int:content_id>/upload/', v1_views.ContentUploadViewV1.as_view(), name='upload_content'),

    # health Check api
    path('health-check/', v1_views.HealthCheckView.as_view(), name='health-check'),
]
