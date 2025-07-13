from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.utils.timezone import now
from django.views.generic import DetailView, ListView
from django_weasyprint import WeasyTemplateResponseMixin

try:
    from openai import OpenAI
except ImportError:

    class OpenAIError(Exception):  # type: ignore[no-redef]
        pass

    class OpenAI:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
            raise OpenAIError("OpenAI package not installed")


from rest_framework.viewsets import ModelViewSet

from apps.main.models import CV
from apps.main.send_pdf_email_task import send_cv_pdf_email_task
from apps.main.serializers import CVSerializer
from utils.languages import TRANSLATION_LANGUAGES
from utils.text_from_cv import serialize_cv_for_translation
from utils.translate import translate_text


def send_cv_pdf_view(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            send_cv_pdf_email_task.delay(pk, email)
            messages.success(request, "CV PDF was successfully sent to your email")
    return redirect("main:cv_detail", pk=pk)


class CVDetailPDFView(WeasyTemplateResponseMixin, DetailView):
    model = CV
    template_name = "main/cv_pdf.html"
    context_object_name = "cv"

    def get_pdf_filename(self) -> str:
        timestamp = now().strftime("%Y-%m-%d_%H-%M")
        return f"{timestamp}_{slugify(self.object.firstname)}_{slugify(self.object.lastname)}.pdf"

    def get_queryset(self) -> Any:  # noqa: PLR6301
        return CV.objects.select_related("contacts").prefetch_related("skills", "projects")


def translate_cv_view(request: HttpRequest, pk: int) -> HttpResponse:
    cv = get_object_or_404(CV, pk=pk)

    if request.method == "POST":
        target_language = request.POST.get("language")
        if target_language not in TRANSLATION_LANGUAGES:
            return HttpResponse("Invalid language", status=400)

        try:
            cv_data = serialize_cv_for_translation(cv)
            translated_data = translate_text(cv_data, target_language)
            context = {
                "cv": cv,
                "translated_cv": translated_data,
                "languages": TRANSLATION_LANGUAGES,
            }
            return render(request, "main/cv_detail.html", context)
        except Exception as e:
            messages.error(request, f"Translation failed: {e!s}")
            return redirect("main:cv_detail", pk=pk)

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
