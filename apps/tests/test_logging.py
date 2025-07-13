import pytest
from audit.models import RequestLog
from django.test import override_settings


@pytest.mark.django_db
def test_logs_get_request(client):
    response = client.get("/")
    assert response.status_code == 200
    log = RequestLog.objects.last()
    assert log.method == "GET"
    assert log.path == "/"


@pytest.mark.django_db
def test_logs_post_request(client):
    response = client.post("/api/cv/", data={}, content_type="application/json")
    log = RequestLog.objects.last()
    assert log.method == "POST"
    assert log.path == "/api/cv/"


@pytest.mark.django_db
@override_settings(MIDDLEWARE=[])
def test_no_logs_without_middleware(client):
    client.get("/")
    assert RequestLog.objects.count() == 0
