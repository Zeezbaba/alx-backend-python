from rest_framework import permissions
from .models import Conversation

class IsOwner(permissions.BasePermission):
    """ custom permission to only allow
    owners of an object to access it
    """
    def object_permissions(self, request, view, obj):
        return obj.user == request.user or obj.sender == request.user or obj.receiver == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users to access the api
    Allow only participants in a conversation to send,
    view, update and delete messages
    """
    def has_permission(self, request, view):
        # Allow only authenticated user
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # allow access only if the user is a participant of the converversation
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
            return request.user in obj.conversation.participants.all()
        retutn False