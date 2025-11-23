from rest_framework import serializers
from .models import User, Conversation, Message


# ---------------------------------
# User Serializer
#----------------------------------
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


# ---------------------------------
# Message Serializer
#----------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_preview = serializers.CharField(source='message_body', read_only=True)
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at', 'message_preview']
        read_only_fields = ['sent_at']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError('Message body cannot be empty')
        return value


# ---------------------------------
# Conversation Serializer
#----------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['created_at']
