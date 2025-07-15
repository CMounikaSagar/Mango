from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Account, User_Profile_Model
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth.password_validation import validate_password
import re
from django.core.validators import validate_email
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError as DjangoValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        username = validated_data['email'].split('@')[0]
        user = Account.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=username,
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )

        # Assign "customer" group
        customer_group, created = Group.objects.get_or_create(name="customer")
        user.groups.add(customer_group)

        # Create default user profile
        User_Profile_Model.objects.create(
            user=user,
            profile_picture='default/default-user.png'
        )

        return user


User = get_user_model()

class JWTLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False, write_only=True)

    def validate(self, data):
        identifier = data.get("identifier")
        password = data.get("password")

        # --- Validate presence ---
        if not identifier:
            raise serializers.ValidationError({"identifier": "This field may not be blank."})
        if not password:
            raise serializers.ValidationError({"password": "This field may not be blank."})

        # --- Email or Phone check ---
        if identifier.isdigit():
            if not re.fullmatch(r'\d{10}', identifier):
                raise serializers.ValidationError({"identifier": "Enter a valid 10-digit phone number."})
            user_filter = {"phone_number": identifier}
        elif '@' in identifier:
            try:
                validate_email(identifier)
            except DjangoValidationError:
                raise serializers.ValidationError({"identifier": "Enter a valid email address."})
            user_filter = {"email": identifier}
        else:
            raise serializers.ValidationError({"identifier": "Enter a valid email or phone number."})

        # --- Fetch user ---
        try:
            user = User.objects.get(**user_filter)
        except User.DoesNotExist:
            raise serializers.ValidationError({"identifier": "User with this identifier does not exist."})

        # --- Password check ---
        if not check_password(password, user.password):
            raise serializers.ValidationError({"password": "Incorrect password."})

        # --- Account status check ---
        if not user.is_active:
            raise serializers.ValidationError({"identifier": "User account is disabled."})

        # --- Generate tokens ---
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
            }
        }
        

# accounts/serializers.py

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    default_error_messages = {
        'bad_token': 'Token is invalid or expired'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()  # blacklists the refresh token
        except TokenError as e:
            print(f"Token error: {e}") 
            raise serializers.ValidationError({
                'refresh': f'Token error: {str(e)}'
            })


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'phone_number',
            'username',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
            'is_admin',
            'is_superadmin'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_admin', 'is_superadmin']