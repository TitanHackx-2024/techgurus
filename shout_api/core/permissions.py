from rest_framework import permissions

class HasRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        required_permission = getattr(view, 'required_permission', None)
        if not required_permission:
            return False
        user_roles = request.user.userrole_set.all()
        for user_role in user_roles:
            if user_role.role.has_permission(required_permission):
                return True
        return False

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'account'):
            return obj.account == request.user.account
        return False

class IsContentCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user

class IsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.userrole_set.filter(role__role_name='Editor').exists()