from django.shortcuts import render
from rest_frame import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import MessageSerializer, ConversationSerializer


# ---------------------------------
# Conversation ViewSet
#---------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
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
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']

    # A function method to add participant to an existion conversation
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        conversation.participants.add(User)
        conversation.save()
        return Response({'message': f'User {user_id} added to conversation.'}, status=status.HTTP_200_OK)


# ---------------------------------
# Message ViewSet
#---------------------------------
class MessageViewSet(viewsets.ModelViewSet):
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
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['sender__first_name', 'sender__last_name', 'message_body']
    ordering_fields = ['sent_at']

    def perform_create(self, serializer):
        '''
        Automatically set the sender to be the current signed in user
        '''
        serializer.save(sender=self.request.user)