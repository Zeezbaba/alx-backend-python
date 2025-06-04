from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """ custom permission to only allow
    owners of an object to access it
    """
    def object_permissions(self, request, view, obj):
        return obj.user == request.user or obj.sender == request.user or obj.receiver == request.user