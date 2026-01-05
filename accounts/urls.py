from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path("profile/", views.profile_view, name="profile"),
    path("change-pfp/", views.change_pfp, name="change_pfp"),
    path("change-username/", views.change_username, name="change_username"),
    path("change-password/", views.change_password, name="change_password"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("profile/testimonial/", views.submit_testimonial, name="submit_testimonial"),
    path("profile/testimonial/edit/", views.edit_testimonial, name="edit_testimonial"),
    path("profile/testimonial/delete/", views.delete_testimonial, name="delete_testimonial"),
    path("update-preferences/", views.update_preferences, name="update_preferences"),
]