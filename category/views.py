from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category
from store.models import Product
from .serializers import *
from django.db.models import Q

class CategoryListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all().order_by('-created_date')
        categories = Category.objects.filter(is_available=True)
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProductsByCategoryAPIView(APIView):
    
    
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)

        # Get query parameters
        search = request.GET.get('search', '')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        sort_by = request.GET.get('sort_by')  # "price-asc", "price-desc", "rating"

        # Base queryset
        products = Product.objects.filter(category=category)

        # Search filter
        if search:
            products = products.filter(
                Q(Product_name__icontains=search) |
                Q(description__icontains=search)
            )

        # Price filter
        if min_price and max_price:
            products = products.filter(Price__gte=min_price, Price__lte=max_price)

        # Sorting
        if sort_by == "price-asc":
            products = products.order_by("Price")
        elif sort_by == "price-desc":
            products = products.order_by("-Price")
        elif sort_by == "rating":
            products = products.order_by("-rating")  # Ensure you have `rating` field
        else:
            products = products.order_by("id")

        # Serialize
        serializer = ProductSerializer(products, many=True, context={'request': request})
        product_data = serializer.data

        # Assign colors
        colors = ["bg-orange-100", "bg-green-100", "bg-blue-100", "bg-yellow-100", "bg-pink-100"]
        for i, product in enumerate(product_data):
            product["color"] = colors[i % len(colors)]

        return Response({
            "category_name": category.category_name,
            "products": product_data
        })

