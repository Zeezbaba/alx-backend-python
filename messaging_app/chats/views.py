from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    """ List and create conversation """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

    def query_set(self):
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

    def query_set(self):
        return Message.objects.filter(conversations__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        # Gets required fields
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')

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
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
