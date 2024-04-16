from django.urls import path, include

from . import views


urlpatterns = [
	path('product/', views.product_list, name='product_list'),
	path('product/<int:pk>/', views.product_detail, name='product_detail'),
	path('category/<int:pk>/', views.category_detail, name='category_detail'),
]
