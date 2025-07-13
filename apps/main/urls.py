from django.urls import path

from main.views import CVListView

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
]

app_name = "main"
