from audit.models import RequestLog
from django.shortcuts import render


def recent_logs_view(request):
    logs = RequestLog.objects.order_by("-timestamp")[:10]
    return render(request, "audit/recent_logs.html", {"logs": logs})
