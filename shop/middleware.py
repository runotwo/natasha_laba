import random
import string

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin


class RequestLoggerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            user = User.objects.create(is_active=False, username=username, password=password)
            print(user)
            login(request, user)
