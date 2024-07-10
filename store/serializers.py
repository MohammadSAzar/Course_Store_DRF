from rest_framework import serializers
from django.utils.text import slugify

from .models import Category, Product, Comment, Cart, CartItem, Customer

DOLLAR_TO_RIAL = 600000

class CategorySerializer(serializers.ModelSerializer):
    # number_of_products = serializers.SerializerMethodField()
    number_of_products = serializers.IntegerField(source='product.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'number_of_products']

    # def get_number_of_products(self, category):
    #     return category.products.count()


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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body']

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id, **validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone_number', 'birth_date']


# ************************* Cart Serializers ****************************** #
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_pk']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)
        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'cart', 'quantity', 'item_total_price']

    def get_item_total_price(self, item):
        return int(item.quantity*item.product.unit_price)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'total_cart_price']
        read_only_fields = ['id', 'items']

    def get_total_cart_price(self, cart):
        price = 0
        items = cart.items.all()
        for item in items:
            price += int(item.quantity*item.product.unit_price)
        return price
