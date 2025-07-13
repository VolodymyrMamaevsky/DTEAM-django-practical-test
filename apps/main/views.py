import tempfile
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.generic import DetailView, ListView

from main.models import CV
from utils.html_to_pdf import generate_pdf


def export_cv_pdf(request, pk):
    cv = get_object_or_404(CV, pk=pk)
    context = {"cv": cv}
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    filename = f"{timestamp}_{slugify(cv.firstname)}_{slugify(cv.lastname)}.pdf"

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmpfile:
        generate_pdf("main/cv_detail.html", context, tmpfile.name)

        response = FileResponse(open(tmpfile.name, "rb"), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class CVListView(ListView):
    model = CV
    template_name = "main/cv_list.html"
    context_object_name = "cv_list"
    queryset = CV.objects.select_related("contacts").prefetch_related("skills", "projects")


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"
