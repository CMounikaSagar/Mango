from django.db import models
from store.models import *
from accounts.models import *
from django.conf import settings

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250,blank=True,null=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        # First, check if the cart is linked to a user.
        if self.user:
            return f"Cart for {self.user.username} (ID: {self.id})"
        # If not, it must be a guest cart.
        return f"Guest Cart (Session: {self._cart_id})"
    
class CartItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('product', 'cart')
    
    def sub_total(self):
        return self.product.Price*self.quantity
    
    def __str__(self):
        return str(self.product)