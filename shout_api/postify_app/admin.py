from django.contrib import admin

# Register your models here.
from .models import Account, User, Role, UserRole, Platform, Content

admin.site.register(Account)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Platform)
admin.site.register(Content)
