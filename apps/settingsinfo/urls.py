from django.urls import path

from apps.settingsinfo.views import SettingsView

urlpatterns = [
    path("", SettingsView.as_view(), name="settings"),
]

app_name = "settingsinfo"
