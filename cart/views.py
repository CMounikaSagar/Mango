# cart/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CartItem,Cart
from store.models import Product
from .serializers import CartItemSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart




class CartAPIView(APIView):
    
    def get(self, request):
        try:
            cart_items = []
            subtotal = 0
            quantity = 0
            tax_rate = 0.05  # 5% tax

            # Use the same logic as POST to find the cart
            if request.user.is_authenticated:
                current_cart_obj = Cart.objects.filter(user=request.user).first()
            else:
                cart_id_str = _cart_id(request)
                current_cart_obj = Cart.objects.filter(cart_id=cart_id_str).first()
                return Response({"error": "No active session."}, status=status.HTTP_400_BAD_REQUEST)

            # If a cart exists for the user/session, get its items
            if current_cart_obj:
                cart_items = CartItem.objects.filter(cart=current_cart_obj)

                for item in cart_items:
                    subtotal += (item.product.Price * item.quantity)
                    quantity += item.quantity

            tax = round(subtotal * tax_rate, 2)
            total = round(subtotal + tax, 2)
            print(f"Subtotal: {subtotal}")
            print(f"Tax: {tax}")
            print(f"Total: {total}")
            serializer = CartItemSerializer(cart_items, many=True)

            return Response({
                'cart_items': serializer.data,
                'subtotal': round(subtotal, 2),
                'tax': tax,
                'total': total,
                'quantity': quantity
            })

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # your_app/views.py

    def post(self, request):
            product_id = request.data.get('product_id')
            
            if not product_id:
                return Response({"error": "Missing product_id"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": f"Product with id {product_id} not found."},
                            status=status.HTTP_404_NOT_FOUND)

            try:
            
                cart = None 

                # --- Part 1: Stably Find the Parent Cart ---
                if request.user.is_authenticated:
                    # For a logged-in user, find the ONE cart linked to their account.
                    # The 'defaults' ensures that if a new cart is created, it also gets the user.
                    cart, _ = Cart.objects.get_or_create(user=request.user, defaults={'user': request.user})
                else:
                    # For a guest, use their session key.
                    session_key = request.session.session_key
                    if not session_key:
                        request.session.create()
                        session_key = request.session.session_key
                    cart, _ = Cart.objects.get_or_create(cart_id=session_key)

                # --- Part 2: Stably Find the Cart Item ---
                # Now that we have a stable 'cart' object, we can find the item.
                # We must provide all the fields that make an item unique for a user.

                # Prepare the lookup parameters.
                lookup_params = {
                    'cart': cart,
                    'product': product,
                }
                # Since user_id is on your CartItem table, we must include it in the lookup
                # for logged-in users to make the 'get' unique and stable.
                if request.user.is_authenticated:
                    lookup_params['user'] = request.user

                cart_item, item_created = CartItem.objects.get_or_create(
                    **lookup_params,
                    defaults={'quantity': 1}
                )

                # If the item was NOT newly created, it means we found an existing one.
                # Now we increase its quantity.
                if not item_created:
                    quantity_to_add = int(request.data.get('quantity', 1))
                    cart_item.quantity += quantity_to_add
                    cart_item.save()

                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_201_CREATED if item_created else status.HTTP_200_OK)

            except Exception as e:
                import traceback
                traceback.print_exc()
                return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
    def delete(self, request):
        print("delete")
        try:
            product_id = request.data.get('product_id')
            action = request.data.get('action', 'remove')

            if not product_id:
                print(product_id)
                return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not request.user.is_authenticated:
                return Response({'error': 'Login required to modify cart.'}, status=status.HTTP_401_UNAUTHORIZED)

            product = get_object_or_404(Product, id=product_id)
            cart_item = CartItem.objects.filter(user=request.user, product=product).first()

            if not cart_item:
                return Response({'message': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)

            if action == 'decrement':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                    return Response({'message': 'Item quantity decremented.'}, status=status.HTTP_200_OK)
                else:
                    cart_item.delete()
                    return Response({'message': 'Item removed from cart because quantity was 1.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                cart_item.delete()
                return Response({'message': 'Item removed from cart.'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Return all cart items + total for checkout."""
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        serializer = CartItemSerializer(cart_items, many=True)
        total_price = sum(item.sub_total() for item in cart_items)
        total_items = sum(item.quantity for item in cart_items)

        return Response({
            'cart_items': serializer.data,
            'total_items': total_items,
            'total_price': total_price
        })