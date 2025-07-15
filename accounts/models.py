from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group,Permission
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.core.validators import (
    RegexValidator, MinLengthValidator, MaxLengthValidator, EmailValidator
)
import re
from django.core.exceptions import ValidationError


def validate_name(value):
    if not value.isalpha():
        raise ValidationError('Name must contain only alphabetic characters.')
def validate_email(value):
        """Ensure email follows the standard format and ends with .com."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail+\.com$'
        
        if not re.match(email_pattern, value):
            raise ValidationError(_("Enter a valid email address "))

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
    first_name = models.CharField(
        max_length=200,
        validators=[
        validate_name,
        MinLengthValidator(3, "First name must be at least 2 characters long."),
        ])
    last_name = models.CharField(
        max_length=200,
        validators=[
            validate_name,
            MinLengthValidator(4,"Last Name should be atleast 4 letter long")
        ])
    username = models.CharField(
        max_length=200, unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message="Username must contain only letters, numbers, and underscores."
            ),
            MinLengthValidator(4, "Username must be at least 4 characters long.")
        ]
        )
    
    email = models.EmailField(max_length=100,unique=True,
                              validators=[
            validate_email
        ])
    phone_number = models.CharField(max_length=10 , unique=True , 
                                    validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits."
            )
        ])
    
    groups = models.ManyToManyField(
        Group,
        related_name='account_users',  # <== changed from default `user_set`
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='account_user_permissions',  # <== changed from default `user_set`
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

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
    street = models.CharField(blank=True,max_length=100,null=True)
    pincode = models.CharField(blank=True,max_length=100,null=True)
    profile_picture = models.ImageField(blank=True,upload_to='useprofilefile/',null=True)
    city = models.CharField(blank=True,max_length=100,null=True)
    state = models.CharField(blank=True,max_length=100,null=True)
    
    def profile_picture_tag(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="50" height="50" />')
        return "No Image"
    profile_picture_tag.short_description = 'Profile Picture'
    
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1},{self.address_line_2}'