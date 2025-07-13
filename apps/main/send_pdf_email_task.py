import tempfile
from pathlib import Path

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_weasyprint.utils import django_url_fetcher
from weasyprint import HTML

from apps.main.models import CV
from CVProject.celery import app


class CVEmailError(Exception):
    pass


@app.task  # type: ignore[misc]
def send_cv_pdf_email_task(cv_id: int, email: str) -> None:
    try:
        cv = CV.objects.select_related("contacts").prefetch_related("skills", "projects").get(id=cv_id)

        html_string = render_to_string("main/cv_pdf.html", {"cv": cv})

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            HTML(
                string=html_string,
                url_fetcher=django_url_fetcher,
                base_url="file://",
            ).write_pdf(tmp_file.name)

            email_subject = f"CV - {cv.firstname} {cv.lastname}"
            email_body = f"Please find attached the CV for {cv.firstname} {cv.lastname}."

            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                to=[email],
            )

            pdf_data = Path(tmp_file.name).read_bytes()
            email_message.attach(
                f"cv_{cv.firstname}_{cv.lastname}.pdf".lower(),
                pdf_data,
                "application/pdf",
            )

            email_message.send(fail_silently=False)

    except CV.DoesNotExist as e:
        raise CVEmailError("CV not found") from e
    except Exception as e:
        raise CVEmailError(f"Failed to send email: {e!s}") from e
