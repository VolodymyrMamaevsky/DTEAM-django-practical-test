from apps.main.models import CV


def serialize_cv_for_translation(cv: CV) -> str:
    skills = ", ".join(skill.name for skill in cv.skills.all())
    projects = ", ".join(p.name for p in cv.projects.all())
    contact = f"Email: {cv.contacts.email}\nPhone: {cv.contacts.phone}\nLinkedIn: {cv.contacts.linkedin or 'N/A'}"

    return (
        f"Name: {cv.firstname} {cv.lastname}\n"
        f"Bio: {cv.bio}\n"
        f"Skills: {skills}\n"
        f"Projects:\n{projects}\n"
        f"Contact:\n{contact}"
    )
