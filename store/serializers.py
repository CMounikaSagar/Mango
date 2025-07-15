# products/serializers.py
from rest_framework import serializers
from .models import Product, Wishlist
from category.models import Category
from accounts.models import Account


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'Product_name', 'slug', 'description', 'Price', 'image',
            'stock', 'is_available', 'category', 'category_name',
            'created_date', 'modified_date'
        ]


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_id']
        extra_kwargs = {'user': {'read_only': True}}
