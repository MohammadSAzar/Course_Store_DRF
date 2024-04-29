from django.urls import path, include

from . import views


urlpatterns = [
	path('product/', views.ProductList.as_view(), name='product_list'),
	path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
	path('category/', views.CategoryList.as_view(), name='category_list'),
	path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
]
