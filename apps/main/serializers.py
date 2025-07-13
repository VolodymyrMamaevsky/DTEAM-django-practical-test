from typing import Any, ClassVar

from rest_framework import serializers

from apps.main.models import CV, Contact, Project, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields: ClassVar[list[str]] = ["id", "name"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields: ClassVar[list[str]] = ["id", "name", "description", "link"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields: ClassVar[list[str]] = ["id", "email", "phone", "linkedin"]


class CVSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    projects = ProjectSerializer(many=True)
    contacts = ContactSerializer()

    class Meta:
        model = CV
        fields: ClassVar[list[str]] = [
            "id",
            "firstname",
            "lastname",
            "bio",
            "skills",
            "projects",
            "contacts",
        ]

    def create(self, validated_data: dict[str, Any]) -> CV:
        contacts_data = validated_data.pop("contacts")
        skills_data = validated_data.pop("skills", [])
        projects_data = validated_data.pop("projects", [])

        contacts = Contact.objects.create(**contacts_data)
        cv = CV.objects.create(contacts=contacts, **validated_data)

        for skill_data in skills_data:
            skill, _ = Skill.objects.get_or_create(name=skill_data["name"])
            cv.skills.add(skill)

        for project_data in projects_data:
            project = Project.objects.create(**project_data)
            cv.projects.add(project)

        return cv

    def update(self, instance: CV, validated_data: dict[str, Any]) -> CV:
        contacts_data = validated_data.pop("contacts", None)
        skills_data = validated_data.pop("skills", [])
        projects_data = validated_data.pop("projects", [])

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update contacts
        if contacts_data:
            contacts = instance.contacts
            for attr, value in contacts_data.items():
                setattr(contacts, attr, value)
            contacts.save()

        # Update skills (replace all)
        instance.skills.clear()
        for skill_data in skills_data:
            skill, _ = Skill.objects.get_or_create(name=skill_data["name"])
            instance.skills.add(skill)

        # Update projects (replace all)
        instance.projects.clear()
        for project_data in projects_data:
            project = Project.objects.create(**project_data)
            instance.projects.add(project)

        instance.save()
        return instance
