from django.urls import path
from . import views

urlpatterns = [
    # Traditional MVT URLs
    path('', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    # DRF API URL
    path('api/products/', views.ProductListAPI.as_view(), name='api_product_list'),
]