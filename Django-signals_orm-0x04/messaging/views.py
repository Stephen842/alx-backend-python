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

    messages = Message.objects.filter(
        sender=request.user,
        receiver=user_id
    ).select_related(
        'sender',
        'receiver',
        'parent_message'
    ).prefetch_related('replies')
    
    conversation = []

    def build_thread(message):
        ''' Recursive function to build a thread tree of replies '''
        return {
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'timestamp': message.timestamp,
            'replies': [build_thread(reply) for reply in message.replies.all()]
        }
    
    root_messages = messages.filter(parent_message__isnull=True)

    for msg in root_messages:
        conversation.append(build_thread(msg))

    return JsonResponse({'threaded_conversation': conversation}, safe=False)


@login_required
def unread_inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id', 'sender', 'content', 'timestamp'
    )

    data = [
        {
            'id': msg.id,
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp,
        }

        for msg in unread_messages
    ]

    return JsonResponse({'unread_messages': data})