from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from raven.contrib.django.raven_compat.models import sentry_exception_handler

from .sample_exceptions import HelloWorldError

class SampleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.just_say = "Lorem Ipsum"
    def process_exception(self, request, exc):
        if isinstance(exc, HelloWorldError):
            sentry_exceptions_handler(request=request)
            return render(request, 'error.html', {
                'error': exc,
                'status': 500,
            })
