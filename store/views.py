from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


# Product Views
class ProductList(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()

    def get_serializer_context(self):
        return {'request': self.request}

# class ProductList(ListCreateAPIView):
#     def get_serializer_class(self):
#         return ProductSerializer
#
#     def get_queryset(self):
#         return Product.objects.select_related('category').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}


# class ProductList(APIView):
#     def get(self, request):
#         product_qs = Product.objects.select_related('category').all()
#         srlz = ProductSerializer(product_qs, context={'request': request}, many=True)
#         return Response(srlz.data)
#
#     def post(self, request):
#         srlz = ProductSerializer(data=request.data)
#         srlz.is_valid(raise_exception=True)
#         srlz.save()
#         return Response(srlz.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         product_qs = Product.objects.select_related('category').all()
#         srlz = ProductSerializer(product_qs, context={'request': request}, many=True)
#         return Response(srlz.data)
#     elif request.method == 'POST':
#         srlz = ProductSerializer(data=request.data)
#         srlz.is_valid(raise_exception=True)
#         srlz.save()
#         return Response(srlz.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        srlz = ProductSerializer(product, context={'request': request})
        return Response(srlz.data)

    def put(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        srlz = ProductSerializer(product, data=request.data)
        srlz.is_valid(raise_exception=True)
        srlz.save()
        return Response(srlz.data)

    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.Count() > 0:
            return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#     if request.method == 'GET':
#         srlz = ProductSerializer(product, context={'request': request})
#         return Response(srlz.data)
#     elif request.method == 'PUT':
#         srlz = ProductSerializer(product, data=request.data)
#         srlz.is_valid(raise_exception=True)
#         srlz.save()
#         return Response(srlz.data)
#     elif request.method == 'DELETE':
#         if product.order_items.Count() > 0:
#             return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Category
class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()


# class CategoryList(APIView):
#     def get(self, request):
#         category_qs = Category.objects.prefetch_related('products').all()
#         srlz = CategorySerializer(category_qs, many=True)
#         return Response(srlz.data)
#
#     def post(self, request):
#         srlz = CategorySerializer(data=request.data)
#         srlz.is_valid(raise_exception=True)
#         srlz.save()
#         return Response(srlz.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'POST'])
# def category_list(request):
#     if request.method == 'GET':
#         category_qs = Category.objects.prefetch_related('products')all()
#         srlz = CategorySerializer(category_qs, many=True)
#         return Response(srlz.data)
#     elif request.method == 'POST':
#         srlz = CategorySerializer(data=request.data)
#         srlz.is_valid(raise_exception=True)
#         srlz.save()
#         return Response(srlz.data, status=status.HTTP_201_CREATED)


class CategoryDetail(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
        srlz = CategorySerializer(category, context={'request': request})
        return Response(srlz.data)

    def put(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
        srlz = CategorySerializer(category, data=request.data)
        srlz.is_valid(raise_exception=True)
        srlz.save()
        return Response(srlz.data)

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
        if category.products.Count() > 0:
            return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail(request, pk):
#     category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
#     if request.method == 'GET':
#         srlz = CategorySerializer(category, context={'request': request})
#         return Response(srlz.data)
#     elif request.method == 'PUT':
#         srlz = CategorySerializer(category, data=request.data)
#         srlz.is_valid(raise_exception=True)
#         srlz.save()
#         return Response(srlz.data)
#     elif request.method == 'DELETE':
#         if category.products.Count() > 0:
#             return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



