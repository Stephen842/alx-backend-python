from django.shortcuts import render
from rest_frame import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import MessageSerializer, ConversationSerializer


# ---------------------------------
# Conversation ViewSet
#---------------------------------
class ConversationViewset(viewsets.ModelViewSet):
    '''
    API endpoint for conversations:
    - List all conversations
    - Retrieve a conversation
    - Create a new conversation
    '''

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]


# ---------------------------------
# Message ViewSet
#---------------------------------
class MessageViewset(viewsets.ModelViewSet):
    '''
    API endpoint for messages:
    - List messages
    - Retrieve a message
    - Create a new message
    '''

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]

    def perform_create(self, serializer):
        '''
        Automatically set the sender to be the current signed in user
        '''
        serializer.save(sender=self.request.user)