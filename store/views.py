from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Category, Comment, Cart, CartItem, Customer, Order, OrderItem
from .serializers import (ProductSerializer, CategorySerializer, CommentSerializer, CartSerializer, CartItemSerializer,
                          AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializer,
                          OrderAdminSerializer, OrderCreateSerializer, OrderUpdateSerializer)
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly
from .paginations import DefaultPagination

from store.signals import order_creation


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # filterset_fields = ['category_id', 'inventory']
    filterset_class = ProductFilter
    ordering_fields = ['name', 'inventory']
    search_fields = ['name', 'category__title']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count() > 0:
            return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk).all()

    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()

    def destroy(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}


class CartModelViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related('items__product').all()
    lookup_value_regex = '[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}'


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        their_id = request.user.id
        customer = Customer.objects.get(user_id=their_id)
        if request.method == 'GET':
            srlz = CustomerSerializer(customer)
            return Response(srlz.data)
        elif request.method == 'PUT':
            srlz = CustomerSerializer(customer, data=request.data)
            srlz.is_valid(raise_exception=True)
            srlz.save()
            return Response(srlz.data)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser]
        return [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        if self.request.user.is_staff:
            return OrderAdminSerializer
        return OrderSerializer

    def get_queryset(self):
        qs = Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product').all()
            )
        ).all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(customer__user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        srlz = OrderCreateSerializer(data=request.data, context={'user_id': self.request.user.id})
        srlz.is_valid(raise_exception=True)
        created_order = srlz.save()

        order_creation.send_robust(self.__class__, order=created_order)

        srlzer = OrderSerializer(created_order)
        return Response(srlzer.data, status=status.HTTP_201_CREATED)


