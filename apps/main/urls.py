from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.main.views import (
    CVDetailPDFView,
    CVDetailView,
    CVListView,
    CVViewSet,
    send_cv_pdf_view,
    translate_cv_view,
)

router = DefaultRouter()
router.register(r"api/cv", CVViewSet, basename="cv")

app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/pdf/", CVDetailPDFView.as_view(), name="cv_pdf"),
    path("cv/<int:pk>/send/", send_cv_pdf_view, name="send_cv_pdf"),
    path("cv/<int:pk>/translate/", translate_cv_view, name="translate_cv"),
]

urlpatterns += router.urls
