from rest_framework import permissions

from advertisements.models import Advertisement


class IsOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method is 'GET':
            return True
        return request.user == obj.creator
