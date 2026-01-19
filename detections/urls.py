from django.urls import path
from . import views

urlpatterns = [
    path("run/", views.run_detections, name="run_detections"),
]
