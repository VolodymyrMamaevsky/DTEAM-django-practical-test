import pytest
from rest_framework.test import APIClient

from apps.main.models import CV, Contact, Project, Skill


@pytest.mark.django_db
class TestCVAPI:
    def setup_method(self):
        self.client = APIClient()

        # Create related objects
        self.contact = Contact.objects.create(email="john@example.com", phone="1234567890")
        self.skill1 = Skill.objects.create(name="Django")
        self.skill2 = Skill.objects.create(name="REST")
        self.project1 = Project.objects.create(
            name="API Service", description="API with Django", link="https://api.example.com"
        )
        self.project2 = Project.objects.create(
            name="Portfolio", description="Personal site", link="https://me.example.com"
        )

        # Create CV with relations
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            bio="Backend Developer",
            contacts=self.contact,
        )
        self.cv.skills.set([self.skill1])
        self.cv.projects.set([self.project1])

    def test_list(self):
        response = self.client.get("/api/cv/")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_retrieve(self):
        response = self.client.get(f"/api/cv/{self.cv.id}/")
        assert response.status_code == 200
        assert response.data["firstname"] == "John"

    def test_create(self):
        data = {
            "firstname": "Alice",
            "lastname": "Smith",
            "bio": "Fullstack Dev",
            "contacts": {
                "email": "alice@testmail.com",
                "phone": "9876543210",
                "linkedin": "https://linkedin.com/in/alice",
            },
            "skills": [{"name": "TestSkill"}, {"name": "TestSkill2"}],
            "projects": [
                {"name": "API Service", "description": "API with Django", "link": "https://api.example.com"},
                {"name": "Portfolio", "description": "Personal site", "link": "https://me.example.com"},
            ],
        }

        response = self.client.post("/api/cv/", data, format="json")
        print(response.data)
        assert response.status_code == 201
        assert CV.objects.filter(firstname="Alice", lastname="Smith").exists()

    def test_update(self):
        data = {
            "firstname": "Updated",
            "lastname": self.cv.lastname,
            "bio": self.cv.bio,
            "contacts": {
                "email": "updated@email.com",
                "phone": "111222333",
                "linkedin": "https://linkedin.com/in/updated",
            },
            "skills": [{"name": "TestSkill"}],
            "projects": [
                {"name": "Updated Project", "description": "New description", "link": "https://updated.example.com"}
            ],
        }

        response = self.client.put(f"/api/cv/{self.cv.id}/", data, format="json")
        print(response.data)
        assert response.status_code == 200
        self.cv.refresh_from_db()
        assert self.cv.firstname == "Updated"
        assert self.cv.contacts.email == "updated@email.com"
        assert self.cv.contacts.phone == "111222333"
        assert self.cv.skills.count() == 1
        assert self.cv.skills.first().name == "TestSkill"
        assert self.cv.projects.first().name == "Updated Project"

    def test_delete(self):
        response = self.client.delete(f"/api/cv/{self.cv.id}/")
        assert response.status_code == 204
        assert not CV.objects.filter(id=self.cv.id).exists()
