from typing import ClassVar

from django.db import models
from django.utils import timezone


class RequestLog(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField(default=200)
    timestamp = models.DateTimeField(default=timezone.now)
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["-timestamp"]

    def __str__(self) -> str:
        return f"{self.method} {self.path} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
