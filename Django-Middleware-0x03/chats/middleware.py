from datetime import datetime
from django.http import HttpResponseForbidden
import os
import time


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
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = {}

    def __call__(self, request):
        if request.path.startswith('/chat') and request.methof == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60
            limit = 5

            # Initialize record for a new IP
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Remove timestamps older than window
            self.ip_requests[ip] = [t for t in self.ip_requests[ip] if now - t < window]

            if len(self.ip_requests[ip]) >= limit:
                return HttpResponseForbidden('Rate limit exceeded: Max 5 messages per minute.')
            
            # Record current timestamp
            self.ip_requests[ip].append(now)

        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip