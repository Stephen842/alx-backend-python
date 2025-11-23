from datetime import datetime
from django.http import HttpResponseForbidden
import os


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        ### This line ensures that the request.log file exists and if it doesn't it should be created
        self.log_file = os.path.join(os.path.dirname(__file__), 'requests.log')
        if not os.path.exists(self.log_file):
            open(self.log_file, 'w').close()

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_line = f'{datetime.now()} - User: {user} - Path: {request.path}\n'

        with open(self.log_file, 'a') as f:
            f.write(log_line)

        response = self.get_response(request)
        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('chat/'):
            current_hour = datetime.now().hour
            if current_hour < 6 or current_hour >= 21:
                return HttpResponseForbidden('Chat is unavailable between 9PM and 6AM.')
            
        response = self.get_response(request)
        return response