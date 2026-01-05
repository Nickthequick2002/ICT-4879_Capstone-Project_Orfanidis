from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard-home'),

    # This paths are used for the product management
    path('products/', views.manage_products, name='dashboard-products'),
    path('products/add/', views.add_product, name='dashboard-add-product'),
    path('products/<int:id>/edit/', views.edit_product, name='dashboard-edit-product'),
    path('products/<int:id>/delete/', views.delete_product, name='dashboard-delete-product'),
    path('users/', views.user_list, name='user_list'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/create/', views.create_blog, name='create_blog'),
    path('blogs/<int:blog_id>/edit/', views.edit_blog, name='dashboard-edit-blog'),
    path('blogs/<int:blog_id>/delete/', views.delete_blog, name='dashboard-delete-blog'),
    path('exercises/', views.dashboard_exercises_list, name='dashboard-exercises'),
    path('exercises/add/', views.dashboard_add_exercise, name='dashboard-add-exercise'),
    path('exercises/<int:exercise_id>/edit/', views.dashboard_edit_exercise, name='dashboard-edit-exercise'),
    path('exercises/<int:exercise_id>/delete/', views.dashboard_delete_exercise, name='dashboard-delete-exercise'),
]