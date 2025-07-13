from django.urls import path

from main.views import CVDetailView, CVListView, export_cv_pdf

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/pdf/", export_cv_pdf, name="cv_pdf"),
]

app_name = "main"
