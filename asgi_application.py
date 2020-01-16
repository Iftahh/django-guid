# flake8: noqa
# TODO: Remove file from repo
from unittest.mock import MagicMock

from asgiref.local import Local
from django.core.handlers.asgi import ASGIHandler
from django.http import HttpResponse

from django_guid.asgi_middleware import ASGIGuidMiddleware


class MockHandler(ASGIHandler):
    """
    Testing subclass of ASGIHandler that has the actual Django response part
    ripped out.
    """

    request_class = MagicMock()
    headers = {}

    def get_response(self, request):
        """
        Fake response
        """
        return HttpResponse('fake')


async def my_application(scope, receive, send):
    """
    My ASGI application. Run with uvicorn asgi_application:my_application --port 8000
    """
    request = MagicMock()
    request.META = {
        'HTTP_PROFILE_ID': 'asd',
        'REQUEST_METHOD': 'POST',
        'HTTP_OPERATING_SYSTEM_VERSION': 'ICE CREAM',
        'HTTP_PLATFORM': 'ANDROID',
        'HTTP_APP_VERSION': '1.0.0',
        'HTTP_USER_AGENT': 'AUTOMATED TEST',
    }
    request.path = '/'
    request.session = {}
    middleware = ASGIGuidMiddleware(request)

    event = await receive()
    middleware.__call__(request)
    print('view guid= ', ASGIGuidMiddleware.get_guid())
    print(Local()._get_context_id().get_name())
    await send({'type': 'http.response.start', 'status': 200})
    await send({'type': 'http.response.body', 'body': b'You ', 'status': 200, 'more_body': False})
