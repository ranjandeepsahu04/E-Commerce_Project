from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('review/<int:product_id>/add/', views.add_review, name='add_review'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Distributor URLs
    path('distributor/dashboard/', views.distributor_dashboard, name='distributor_dashboard'),
    path('distributor/product/add/', views.add_product, name='add_product'),
    path('distributor/product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('distributor/product/<int:pk>/delete/', views.delete_product, name='delete_product'),

]