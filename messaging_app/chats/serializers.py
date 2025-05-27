from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        ]

    def validate_email(self, value):
        if "@example.com" in value:
            raise serializers.ValidationError("Emails from example.com are not allowed")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'sender_email',
            'message_body',
            'sent_at',
        ]

    def get_sender_email(self, obj):
        return obj.sender.email

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]