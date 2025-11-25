from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Message


@require_http_methods(['POST'])
def delete_user(request):
    '''Allows currently authenticated user to delete their account.'''
    if not request.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = request.user
    logout(request)
    user.delete()

    return JsonResponse({'message': 'User deleted successfully'})


@login_required
def threaded_conversation(request, user_id):
    ''' Retrieve all messages between the current user and another user, optimizing database querying '''

    messages = (
        Message.objects.filter(
            sender = request.user,
            reciever_id = user_id
        )
        |
        Message.objects.filter(
            sender_id = user_id,
            reciever = request.user
        )
    )

    messages = messages.select_related('sender', 'reciever', 'parent_message') \
                        .prefetch_related('replies')
    
    conversation = []

    def build_thread(message):
        ''' Recursive function to build a thread tree of replies '''
        return {
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'reciever': message.reciever.username,
            'timestamp': message.timestamp,
            'replies': [build_thread(reply) for reply in message.replies.all()]
        }
    
    root_messages = messages.filter(parent_message__isnull=True)

    for msg in root_messages:
        conversation.append(build_thread(msg))

    return JsonResponse({'threaded_conversation': conversation}, safe=False)