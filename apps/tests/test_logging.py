import pytest
from django.test.client import Client
from django.urls import reverse

from apps.audit.models import RequestLog


@pytest.mark.django_db
def test_logs_get_request(client: Client) -> None:
    client.get(reverse("main:cv_list"))
    log = RequestLog.objects.last()
    assert log is not None
    assert log.method == "GET"
    assert log.path == "/"
    assert log.status_code == 200


@pytest.mark.django_db
def test_logs_post_request(client: Client) -> None:
    client.post("/api/cv/", data={}, content_type="application/json")
    log = RequestLog.objects.last()
    assert log is not None
    assert log.method == "POST"
    assert log.path == "/api/cv/"
    assert log.status_code == 400


@pytest.mark.django_db
def test_recent_logs_view(client: Client) -> None:
    client.get(reverse("main:cv_list"))
    client.get("/api/cv/")
    client.post("/api/cv/", data={}, content_type="application/json")

    response = client.get(reverse("audit:recent_logs"))
    assert response.status_code == 200
    assert b"Recent Requests" in response.content

    logs = response.context["logs"]
    assert len(logs) > 0
    assert isinstance(logs[0], RequestLog)
