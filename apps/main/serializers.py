from rest_framework import serializers

from main.models import CV, Contact, Project, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "link"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "email", "phone", "linkedin"]


class CVSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    projects = ProjectSerializer(many=True)
    contacts = ContactSerializer()

    class Meta:
        model = CV
        fields = [
            "id",
            "firstname",
            "lastname",
            "bio",
            "skills",
            "projects",
            "contacts",
        ]

    def create(self, validated_data):
        contacts_data = validated_data.pop("contacts")
        skills_data = validated_data.pop("skills", [])
        projects_data = validated_data.pop("projects", [])

        contact = Contact.objects.create(**contacts_data)
        cv = CV.objects.create(contacts=contact, **validated_data)

        for skill_data in skills_data:
            skill, _ = Skill.objects.get_or_create(**skill_data)
            cv.skills.add(skill)

        for project_data in projects_data:
            project, _ = Project.objects.get_or_create(**project_data)
            cv.projects.add(project)

        return cv

    def update(self, instance, validated_data):
        contacts_data = validated_data.pop("contacts", None)
        skills_data = validated_data.pop("skills", [])
        projects_data = validated_data.pop("projects", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if contacts_data:
            Contact.objects.filter(pk=instance.contacts.pk).update(**contacts_data)

        instance.skills.clear()
        for skill_data in skills_data:
            skill, _ = Skill.objects.get_or_create(**skill_data)
            instance.skills.add(skill)

        instance.projects.clear()
        for project_data in projects_data:
            project, _ = Project.objects.get_or_create(**project_data)
            instance.projects.add(project)

        return instance
