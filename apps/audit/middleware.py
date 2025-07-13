from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from apps.audit.models import RequestLog


class RequestLoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        # Log the request
        method = request.method
        if method is not None:
            RequestLog.objects.create(
                path=request.path,
                method=method,
                status_code=response.status_code,
                timestamp=timezone.now(),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                ip_address=self.get_client_ip(request),
            )

        return response

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str | None:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        return x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
