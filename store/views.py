from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Category, Comment
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer
from .filters import ProductFilter


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # filterset_fields = ['category_id', 'inventory']
    filterset_class = ProductFilter
    ordering_fields = ['name', 'inventory']
    search_fields = ['name', 'category__title']

    # def get_queryset(self):
    #     queryset = Product.objects.select_related('category').all()
    #     category_id_param = self.request.query_params.get('category_id')
    #     if category_id_param is not None:
    #         queryset = queryset.filter(category_id=category_id_param)
    #     return queryset

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


# Product Views
# class ProductList(ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         if product.order_items.count() > 0:
#             return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Category views
class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()

    def destroy(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class CategoryList(ListCreateAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products').all()
#
#
# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products').all()
#
#     def delete(self, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
#         if category.products.count() > 0:
#             return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ************************* Commented Views ****************************** #
# Product Views

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


# class ProductDetail(APIView):
#     def get(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category').all(), pk=pk)
#         srlz = ProductSerializer(product)
#         return Response(srlz.data)
#
#     def put(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category').all(), pk=pk)
#         srlz = ProductSerializer(product, data=request.data)
#         srlz.is_valid(raise_exception=True)
#         srlz.save()
#         return Response(srlz.data)
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category').all(), pk=pk)
#         if product.order_items.Count() > 0:
#             return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product.objects.select_related('category').all(), pk=pk)
#     if request.method == 'GET':
#         srlz = ProductSerializer(product)
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


# class CategoryDetail(APIView):
#     def get(self, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
#         srlz = CategorySerializer(category, context={'request': request})
#         return Response(srlz.data)
#
#     def put(self, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
#         srlz = CategorySerializer(category, data=request.data)
#         srlz.is_valid(raise_exception=True)
#         srlz.save()
#         return Response(srlz.data)
#
#     def delete(self, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products').all(), pk=pk)
#         if category.products.Count() > 0:
#             return Response({'error': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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





