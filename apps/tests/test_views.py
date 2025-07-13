import pytest
from django.test.client import Client
from django.urls import reverse

from apps.main.models import CV, Contact, Project, Skill


@pytest.fixture
def setup_cv_data() -> CV:
    skill = Skill.objects.create(name="TestSkill")
    project = Project.objects.create(name="TestProject", description="Some description", link="https://link.com")
    contact = Contact.objects.create(email="test@example.com", phone="1234567890")
    cv = CV.objects.create(firstname="John", lastname="Doe", bio="Test bio", contacts=contact)
    cv.skills.add(skill)
    cv.projects.add(project)
    return cv


@pytest.mark.django_db
def test_cv_detail_view(client: Client) -> None:
    skill = Skill.objects.create(name="TestSkill")
    project = Project.objects.create(name="TestProject", description="Some description", link="https://link.com")
    contact = Contact.objects.create(email="test@example.com", phone="1234567890")
    cv = CV.objects.create(firstname="John", lastname="Doe", bio="Test bio", contacts=contact)
    cv.skills.add(skill)
    cv.projects.add(project)

    response = client.get(reverse("main:cv_detail", kwargs={"pk": cv.id}))
    assert response.status_code == 200
    assert b"John Doe" in response.content
    assert b"Test bio" in response.content
    assert b"TestSkill" in response.content
    assert b"TestProject" in response.content
    assert b"test@example.com" in response.content


@pytest.mark.django_db
def test_cv_list_view(client: Client) -> None:
    # Create test data using fixture
    setup_cv_data()

    response = client.get(reverse("main:cv_list"))
    assert response.status_code == 200
    assert b"John Doe" in response.content
