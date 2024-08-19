from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductModelViewSet, basename='product')
router.register('categories', views.CategoryModelViewSet, basename='category')
router.register('carts', views.CartModelViewSet, basename='cart')
router.register('customers', views.CustomerViewSet, basename='customer')
router.register('orders', views.OrderViewSet, basename='order')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comments')

cart_item_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_item_router.register('items', views.CartItemModelViewSet, basename='cart-items')


urlpatterns = router.urls + products_router.urls + cart_item_router.urls

# urlpatterns = [
# 	path('product/', views.ProductList.as_view(), name='product_list'),
# 	path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
# 	path('category/', views.CategoryList.as_view(), name='category_list'),
# 	path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
# ]
