import pytest
from django.urls import reverse
from main.models import CV, Contact, Project, Skill


@pytest.mark.django_db
def test_cv_list_view(client):
    url = reverse("main:cv_list")
    response = client.get(url)
    assert response.status_code == 200
    assert "Available CVs" in response.content.decode()


@pytest.mark.django_db
def test_cv_detail_view(client, django_user_model):
    skill = Skill.objects.create(name="TestSkill")
    project = Project.objects.create(name="TestProject", description="Some description", link="https://link.com")
    contact = Contact.objects.create(email="test@example.com", phone="+380999999999")

    cv = CV.objects.create(firstname="Test", lastname="User", bio="Just a test CV", contacts=contact)
    cv.skills.add(skill)
    cv.projects.add(project)

    url = reverse("main:cv_detail", kwargs={"pk": cv.pk})
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Test User" in content
    assert "Just a test CV" in content
    assert "TestSkill" in content
    assert "TestProject" in content
