from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.html import mark_safe

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, username, email, first_name, last_name, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone_number=phone_number,
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        # user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, email, first_name, last_name, password=None):
        user = self.create_user(
            phone_number=phone_number,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=10, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'  # Login using phone number
    REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class User_Profile_Model(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True,max_length=100)
    address_line_2 = models.CharField(blank=True,max_length=100)
    profile_picture = models.ImageField(blank=True,upload_to='useprofilefile/')
    city = models.CharField(blank=True,max_length=100)
    state = models.CharField(blank=True,max_length=100)
    
    def profile_picture_tag(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="50" height="50" />')
        return "No Image"
    profile_picture_tag.short_description = 'Profile Picture'
    
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1},{self.address_line_2}'