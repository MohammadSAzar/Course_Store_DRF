from rest_framework import serializers
from django.utils.text import slugify

from .models import Category, Product

DOLLAR_TO_RIAL = 600000

class CategorySerializer(serializers.ModelSerializer):
    number_of_products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'number_of_products']

    def get_number_of_products(self, category):
        return category.products.Count()

class ProductSerializer(serializers.ModelSerializer):
    rial_unit_price = serializers.SerializerMethodField()
    # category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price', 'rial_unit_price', 'category', 'inventory', 'description']

    def get_rial_unit_price(self, product):
        return int(product.unit_price*DOLLAR_TO_RIAL)

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product

