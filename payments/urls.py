from django.urls import path
from . import views

urlpatterns = [
    path("membership/upgrade/", views.membership_upgrade, name="membership_upgrade"),
    path('success/', views.membership_success, name='membership_success'),
]
