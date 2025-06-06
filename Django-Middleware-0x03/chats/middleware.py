import logging
from datetime import datetime
from django.http import HttpResponseForbidden

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

        # Allow access only between 18:00(6pm) and 21:00(9pm)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to the chat is only allowed between 6pm and 9pm")

        # Continue the process
        response = self.get_response(request)
        return response