from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import CVDetailView, CVListView, CVViewSet, export_cv_pdf

router = DefaultRouter()
router.register(r"api/cv", CVViewSet, basename="cv")

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/pdf/", export_cv_pdf, name="cv_pdf"),
]

urlpatterns += router.urls

app_name = "main"
