from django.urls import path

from apps.settingsinfo.views import SettingsView

app_name = "settingsinfo"

urlpatterns = [
    path("", SettingsView.as_view(), name="settings"),
]
