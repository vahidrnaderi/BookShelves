"""AAP custom middleware."""
from django.conf import settings


class CorsMiddleware:
    """CORS middleware."""

    def __init__(self, get_response):
        """Initialize the class."""
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers["Access-Control-Allow-Origin"] = settings.CORS_ALLOWED_HOST
        return response
