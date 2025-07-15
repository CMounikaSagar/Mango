# products/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Product, Wishlist
from .serializers import ProductSerializer, WishlistSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListCreateView(APIView):
    """
    GET: List products with pagination (8 per page)
    POST (optional): Create a new product
    """
    def get(self, request):
        products = Product.objects.all().order_by('-created_date')
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

class ProductDetailView(APIView):
    """
    GET: Retrieve single product details by ID
    """
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class WishlistView(APIView):
    """
    GET: List wishlist items for current user.
    POST: Toggle wishlist item (add if not present, remove if present).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data)


    def post(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id)
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

        if wishlist_item:
            wishlist_item.delete()
            return Response({'message': 'Product removed from wishlist.'}, status=status.HTTP_200_OK)
        else:
            Wishlist.objects.create(user=request.user, product=product)
            return Response({'message': 'Product added to wishlist.'}, status=status.HTTP_201_CREATED)