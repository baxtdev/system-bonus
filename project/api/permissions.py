from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_superuser