from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, filters
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    """ List and create conversation """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        # Gets participants IDs
        participant_ids = request.data.get('participants')
        if not participant_ids or not isinstance(participant_ids, list):
            return Response({"error": "Particants  must be a list of user ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            participants = User.objects.filter(user_id__in=participant_ids)
            if request.user not in participants:
                # Automatically add the user to participants
                participants = list(participants) + [request.user]
        except Exception:
            return Response({"error": "Invalid participants lists"},
                            status=status.HTTP_400_BAD_REQUEST)

        # create the conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """ List and send messages in a conversation """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        return (
            Message.objects
            .filter(conversation__participants=self.request.user)
            .select_related('sender', 'conversation', 'parent_message')
            .prefetch_related('replies'))

    def create(self, request, *args, **kwargs):
        # Gets required fields
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')
        parent_id = request.data.get('parent_message')

        if not all([conversation_id, sender_id, message_id]):
            return Response({"error": "conversation_id, sender_id, message_id are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
        except (Conversation.DoesNotExist, User.DoesNotExist):
            return Response({"error": "Invalid conversation or sender ID"},
            status=status.HTTP_400_BAD_REQUEST)

        if sender not in conversation.participants.all():
            return Response({"error": "Forbidden"},
            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body,
            parent_message=parent_message
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')

def get_threaded_replies(message):
    thread = []

    def recurse(msg, depth=0):
        thread.append((depth, msg))
        for reply in msg.replies.all():
            recurse(reply, depth + 1)

    recurse(message)
    return thread