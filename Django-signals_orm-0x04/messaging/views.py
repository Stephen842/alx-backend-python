from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout


@require_http_methods(['POST'])
def delete_user(request):
    '''Allows currently authenticated user to delete their account.'''
    if not request.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = request.user
    logout(request)
    user.delete()

    return JsonResponse({'message': 'User deleted successfully'})