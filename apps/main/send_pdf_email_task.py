import tempfile

from django.core.mail import EmailMessage

from apps.main.models import CV
from CVProject.celery import app
from utils.html_to_pdf import generate_pdf


@app.task
def send_cv_pdf_email_task(cv_id, email):
    cv = CV.objects.select_related("contacts").prefetch_related("skills", "projects").get(id=cv_id)

    context = {"cv": cv}
    template_name = "main/cv_detail.html"

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmpfile:
        generate_pdf(template_name, context, tmpfile.name)

        mail = EmailMessage(subject="CV PDF", body="Here is the exported CV.", to=[email])
        mail.attach("cv.pdf", tmpfile.read(), "application/pdf")
        mail.send()
