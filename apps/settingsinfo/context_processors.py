from typing import Any

from django.conf import settings
from django.http import HttpRequest


def settings_context(_: HttpRequest) -> dict[str, Any]:
    return {
        "DEBUG": settings.DEBUG,
        "ALLOWED_HOSTS": settings.ALLOWED_HOSTS,
    }
