from django.urls import path
from . import views

app_name = "import_manager"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("template/", views.download_template, name="download_template"),
]
