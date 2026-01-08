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
    path("update-details/", views.update_account_details, name="update_account_details"),
    path("update-pfp-ajax/", views.update_pfp_ajax, name="update_pfp_ajax"),
    path("edit-testimonial-ajax/", views.edit_testimonial_ajax, name="edit_testimonial_ajax"),
    path("submit-testimonial-ajax/", views.submit_testimonial_ajax, name="submit_testimonial_ajax"),
    path("delete-testimonial-ajax/", views.delete_testimonial_ajax, name="delete_testimonial_ajax"),
    path("progress-data/", views.get_progress_data, name="get_progress_data"),
    path("log-progress/", views.log_progress_ajax, name="log_progress_ajax"),
]