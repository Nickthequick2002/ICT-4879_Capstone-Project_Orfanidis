from django.urls import path
from . import views

urlpatterns = [
    path("", views.mycals_view, name="mycals"),
    path("delete/<int:pk>/", views.delete_food, name="delete_food"),
]
