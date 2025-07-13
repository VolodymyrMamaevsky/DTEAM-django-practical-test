from django.views.generic import ListView

from main.models import CV


class CVListView(ListView):
    model = CV
    template_name = "main/cv_list.html"
    context_object_name = "cv_list"
    queryset = CV.objects.select_related("contacts").prefetch_related("skills", "projects")
