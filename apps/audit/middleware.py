from django.utils.deprecation import MiddlewareMixin
from audit.models import RequestLog


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if (
                request.path.startswith("/static/")
                or request.path.startswith("/admin/")
        ):
            return

        RequestLog.objects.create(
            method=request.method,
            path=request.path,
            query_string=request.META.get("QUERY_STRING", ""),
            remote_addr=self.get_client_ip(request),
            user=request.user if request.user.is_authenticated else None
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
