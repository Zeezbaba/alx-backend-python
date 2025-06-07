import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # set up a logger that writes to a file 'requests.log'
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        # Add handler only ones to avoid duplication when reloading code
        if not self.logger.handlers:
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        # Get the user who made the request
        # or anonymous if not logged in
        user = request.user if request.user.is_authenticated else 'Anonymous'
        # Log the current time, user and request path
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Get the response for this request from the next layer/middleware
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server hour
        current_hour = datetime.now().hour

        # Allow access only between 09:00(9am) and 18:00(6pm)
        if current_hour < 8 or current_hour >= 18:
            return HttpResponseForbidden("Access to the chat is only allowed between 9am and 6pm")

        # Continue the process
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store IP address and their timestamps
        self.requests = {}

    def __call__(self, request):
        # rate-limit POST request
        if request.method == 'POST' and '/messages' in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            # Get list of previous timestamp or start new
            request_times = self.requests.get(ip, [])

            # Get previous request times for the IP address or initialize a list
            request_times = [t for t in request_times if now - t < 60]

            if len(request_times) >= 5:
                return JsonResponse({
                    'error': 'Rate Limit Exceeded. Max 5 messages per minute.'
                }, status=429)

            # Store the updated timestamp list
            request_times.append(now)
            self.requests[ip] = request_times

            # Proceed to next middleware
        return self.get_response(request)

    def get_client_ip(self, request):
        # Get IP address from headers or remote address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip