# core/admin.py
from django.contrib import admin
from .models import Account, User, Role, UserRole, Platform, Content, ContentPlatform

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_status', 'created_at')
    search_fields = ('account_name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'account', 'user_status')
    search_fields = ('username', 'email')
    list_filter = ('account', 'user_status')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'account', 'content_type', 'status', 'created_by', 'editor')
    list_filter = ('account', 'content_type', 'status')
    search_fields = ('title', 'description')

@admin.register(ContentPlatform)
class ContentPlatformAdmin(admin.ModelAdmin):
    list_display = ('content', 'platform', 'upload_status')
    list_filter = ('platform', 'upload_status')