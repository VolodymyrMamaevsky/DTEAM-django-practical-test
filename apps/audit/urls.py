from audit.views import recent_logs_view
from django.urls import path

urlpatterns = [
    path("logs/", recent_logs_view, name="recent_logs"),
]

app_name = "audit"
