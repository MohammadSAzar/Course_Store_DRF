from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        product_qs = Product.objects.select_related('category').all()
        srlz = ProductSerializer(product_qs, context={'request': request}, many=True)
        return Response(srlz.data)
    elif request.method == 'POST':
        srlz = ProductSerializer(data=request.data)
        srlz.is_valid(raise_exception=True)
        srlz.save()
        return Response(srlz.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    if request.method == 'GET':
        srlz = ProductSerializer(product, context={'request': request})
        return Response(srlz.data)
    elif request.method == 'PUT':
        srlz = ProductSerializer(product, data=request.data)
        srlz.is_valid(raise_exception=True)
        srlz.save()
        return Response(srlz.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        category_qs = Category.objects.annotate(product_count=Count('products')).all()
        srlz = CategorySerializer(category_qs, context={'request': request}, many=True)
        return Response(srlz.data)
    elif request.method == 'POST':
        srlz = CategorySerializer(data=request.data)
        srlz.is_valid(raise_exception=True)
        srlz.save()
        return Response(srlz.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=pk)
    if request.method == 'GET':
        srlz = CategorySerializer(category, context={'request': request})
        return Response(srlz.data)
    elif request.method == 'PUT':
        srlz = CategorySerializer(category, data=request.data)
        srlz.is_valid(raise_exception=True)
        srlz.save()
        return Response(srlz.data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



