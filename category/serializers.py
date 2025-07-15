from rest_framework import serializers
from .models import Category
from store.models import Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'description', 'cat_image', 'is_available']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name', read_only=True)
    image = serializers.ImageField(use_url=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'Product_name',
            'slug',
            'description',
            'Price',
            'stock',
            'is_available',
            'image',
            'category',
            'created_date',
            'modified_date',
            'url',
        ]

    def get_url(self, obj):
        return obj.get_url()
