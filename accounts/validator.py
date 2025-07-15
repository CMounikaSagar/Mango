import re
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()

def validate_email_or_phone(identifier):
    """
    Validates if the identifier is a valid email or phone number.
    Raises a ValidationError if not valid.
    """
    if identifier.isdigit():
        if not re.fullmatch(r'\d{10}', identifier):
            raise serializers.ValidationError("Enter a valid 10-digit phone number.")
    elif '@' in identifier:
        try:
            validate_email(identifier)
        except DjangoValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
    else:
        raise serializers.ValidationError("Enter a valid email or phone number.")

def validate_required_fields(data, fields):
    """
    Checks if required fields are present and not empty in data.
    Raises a ValidationError with appropriate message for each missing field.
    """
    errors = {}
    for field in fields:
        value = data.get(field)
        if not value or str(value).strip() == "":
            errors[field] = f"{field.replace('_', ' ').capitalize()} is required."
    if errors:
        raise serializers.ValidationError(errors)

def validate_user_and_password(identifier, password):
    """
    Validates that a user exists for the given identifier and the password is correct.
    """
    # Try to get user by email or phone number
    try:
        if identifier.isdigit():
            user = User.objects.get(phone_number=identifier)
        else:
            user = User.objects.get(email=identifier)
    except User.DoesNotExist:
        raise serializers.ValidationError("User with given email or phone does not exist.")

    if not user.check_password(password):
        raise serializers.ValidationError("Incorrect password.")

    return user  # If needed later
