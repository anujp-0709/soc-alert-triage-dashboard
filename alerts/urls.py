from django.urls import path
from . import views

urlpatterns = [
    path("", views.alert_list, name="alert_list"),
    path("<int:alert_id>/", views.alert_detail, name="alert_detail"),
    path("<int:alert_id>/pdf/", views.alert_pdf, name="alert_pdf"),

]
