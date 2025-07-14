from django.urls import path

from apps.audit.views import recent_logs_view

app_name = "audit"

urlpatterns = [
    path("logs/", recent_logs_view, name="recent_logs"),
]
