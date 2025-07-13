from django.db import models
from django.db.models import CASCADE


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.name


class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.email


class CV(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    bio = models.TextField()
    skills = models.ManyToManyField(Skill, related_name="cvs")
    projects = models.ManyToManyField(Project, related_name="cvs")
    contacts = models.OneToOneField(Contact, on_delete=CASCADE, related_name="cv")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
