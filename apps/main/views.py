import tempfile
from pathlib import Path
from typing import Any

from django.contrib import messages
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.utils.timezone import now
from django.views.generic import DetailView, ListView

# Import OpenAIError with handling of possible import errors
try:
    from openai.exceptions import OpenAIError
except ImportError:
    try:
        from openai.error import OpenAIError  # type: ignore[no-redef]
    except ImportError:
        # Define class only if import failed
        class OpenAIError(Exception):  # type: ignore[no-redef]
            pass


from rest_framework.viewsets import ModelViewSet

from apps.main.models import CV
from apps.main.send_pdf_email_task import send_cv_pdf_email_task
from apps.main.serializers import CVSerializer
from utils.html_to_pdf import generate_pdf
from utils.languages import TRANSLATION_LANGUAGES
from utils.text_from_cv import serialize_cv_for_translation
from utils.translate import translate_text


def export_cv_pdf(_: HttpRequest, pk: int) -> FileResponse:
    cv = get_object_or_404(CV, pk=pk)
    context = {"cv": cv}
    timestamp = now().strftime("%Y-%m-%d_%H-%M")

    filename = f"{timestamp}_{slugify(cv.firstname)}_{slugify(cv.lastname)}.pdf"

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmpfile:
        generate_pdf("main/cv_detail.html", context, tmpfile.name)

        with Path(tmpfile.name).open("rb") as pdf_file:
            response = FileResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response


def send_cv_pdf_view(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            send_cv_pdf_email_task.delay(pk, email)
            messages.success(request, "CV PDF was successfully sent to your email")
    return redirect("main:cv_detail", pk=pk)


def translate_cv_view(request: HttpRequest, pk: int) -> HttpResponse:
    cv = get_object_or_404(CV, pk=pk)
    if request.method == "POST":
        lang = request.POST.get("language")
        if lang:
            try:
                text = serialize_cv_for_translation(cv)
                translated = translate_text(text, lang)
                return render(
                    request,
                    "main/cv_detail.html",
                    {"cv": cv, "translated_cv": translated, "languages": TRANSLATION_LANGUAGES},
                )
            except OpenAIError:
                messages.error(request, "Translation failed")
    else:
        messages.error(request, "No language selected.")
    return redirect("main:cv_detail", pk=pk)


class CVListView(ListView):
    model = CV
    template_name = "main/cv_list.html"
    context_object_name = "cv_list"
    queryset = CV.objects.select_related("contacts").prefetch_related("skills", "projects")


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["languages"] = TRANSLATION_LANGUAGES
        return context


class CVViewSet(ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
