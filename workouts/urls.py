from django.urls import path
from . import views

urlpatterns = [
    path("<int:program_id>/start/", views.program_detail, name="program_detail"),
]