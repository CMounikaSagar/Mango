from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import *
from django.contrib.auth.models import User

# Create your models here.  
class Product(models.Model):
    Product_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=500,blank=True)
    Price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    def get_url(self):
        return reverse('products-by-category',args=[self.category.id])
        
        
    def __str__(self):
        return self.Product_name
    

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # added_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.Product_name}"
