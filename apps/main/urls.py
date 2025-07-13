from django.urls import path

from main.views import CVDetailView, CVListView

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
]

app_name = "main"
