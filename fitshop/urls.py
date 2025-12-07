from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_home, name='fitshop'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path("cart/", views.view_cart, name="view_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='payment_success'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
]
