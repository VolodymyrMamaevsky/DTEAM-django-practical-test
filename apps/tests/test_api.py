import pytest
from rest_framework.test import APIClient

from apps.main.models import CV, Contact, Project, Skill


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCVAPI:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.skill1 = Skill.objects.create(name="Python")
        self.skill2 = Skill.objects.create(name="Django")
        self.project1 = Project.objects.create(
            name="Project1",
            description="Description1",
            link="https://example1.com",
        )
        self.project2 = Project.objects.create(
            name="Project2",
            description="Description2",
            link="https://example2.com",
        )
        self.contact = Contact.objects.create(
            email="john@example.com",
            phone="+1234567890",
            linkedin="https://linkedin.com/in/john",
        )
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            bio="Developer",
        )
        self.cv.skills.add(self.skill1)
        self.cv.projects.add(self.project1)
        self.cv.contacts = self.contact
        self.cv.save()
        self.client = APIClient()

    def test_get_cv_list(self) -> None:
        response = self.client.get("/api/cv/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["firstname"] == "John"

    def test_get_cv_detail(self) -> None:
        response = self.client.get(f"/api/cv/{self.cv.id}/")
        assert response.status_code == 200
        assert response.data["firstname"] == "John"
        assert response.data["lastname"] == "Doe"

    def test_create_cv(self) -> None:
        data = {
            "firstname": "Alice",
            "lastname": "Smith",
            "bio": "Designer",
            "skills": [{"name": "UI/UX"}, {"name": "Figma"}],
            "projects": [
                {"name": "Design System", "description": "Company design system", "link": "https://design.com"}
            ],
            "contacts": {
                "email": "alice@example.com",
                "phone": "+9876543210",
                "linkedin": "https://linkedin.com/in/alice",
            },
        }
        response = self.client.post("/api/cv/", data, format="json")
        assert response.status_code == 201
        assert CV.objects.filter(firstname="Alice", lastname="Smith").exists()
        new_cv = CV.objects.get(firstname="Alice")
        assert new_cv.skills.count() == 2
        assert new_cv.projects.count() == 1
        assert new_cv.contacts.email == "alice@example.com"

    def test_update_cv(self) -> None:
        data = {
            "firstname": "John",
            "lastname": "Smith",  # Changed
            "bio": "Senior Developer",  # Changed
            "skills": [{"name": "Python"}, {"name": "FastAPI"}],  # Changed Django to FastAPI
            "projects": [
                {
                    "name": "Project1",
                    "description": "Updated description",
                    "link": "https://example1.com",
                }  # Changed description
            ],
            "contacts": {
                "email": "john.smith@example.com",
                "phone": "+1234567890",
                "linkedin": "https://linkedin.com/in/john",
            },
        }
        response = self.client.put(f"/api/cv/{self.cv.id}/", data, format="json")
        assert response.status_code == 200
        self.cv.refresh_from_db()
        assert self.cv.lastname == "Smith"
        assert self.cv.bio == "Senior Developer"
        assert self.cv.skills.filter(name="FastAPI").exists()
        assert not self.cv.skills.filter(name="Django").exists()
        project = self.cv.projects.first()
        assert project is not None
        assert project.description == "Updated description"
        assert self.cv.contacts.email == "john.smith@example.com"

    def test_delete_cv(self) -> None:
        response = self.client.delete(f"/api/cv/{self.cv.id}/")
        assert response.status_code == 204
        assert not CV.objects.filter(id=self.cv.id).exists()
