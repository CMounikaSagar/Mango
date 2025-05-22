from django.db import models
from django.utils import timezone
from accounts.models import *
import random

# Create your models here.
class OTP(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.save()

    def is_expired(self):
        return (timezone.now() - self.created_at).seconds > 300  # 5 mins