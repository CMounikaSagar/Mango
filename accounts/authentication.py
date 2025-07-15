from django.contrib.auth.backends import ModelBackend
from .models import Account

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Account = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        user = None
        if identifier:
            try:
                if identifier.isdigit():
                    user = Account.objects.get(phone_number=identifier)
                else:
                    user = Account.objects.get(email=identifier)
            except Account.DoesNotExist:
                return None

            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
