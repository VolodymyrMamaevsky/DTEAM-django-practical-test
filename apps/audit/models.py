from django.contrib.auth.models import User
from django.db import models


class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=512)
    query_string = models.TextField(blank=True)
    remote_addr = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.method} {self.path}"
