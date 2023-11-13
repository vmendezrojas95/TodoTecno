from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = AnonymousUser()
        if hasattr(request, 'user'):
            request._cached_user = request.user
    return request._cached_user

class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))
        response = self.get_response(request)
        return response
