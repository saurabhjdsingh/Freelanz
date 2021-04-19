from django.db import models
from django.contrib.auth.models import User
from projects.models import CompletedOrder
from dashboard.models import Profile


class Payment(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    payment_amount = models.CharField(max_length=200, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True, unique=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    captured = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.profile.user.username


class Refund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField(default=0)


class VirtualCurrency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField(default=0)


class Tempwallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField(default=0)


class AccountDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    account_id = models.CharField(max_length=255, blank=True, null=True,)
    bank_name = models.CharField(max_length=255)
    account_number = models.IntegerField(null=True, unique=True)
    name = models.CharField(max_length=240)
    ifsc_code = models.CharField(max_length=11)
    verified = models.BooleanField(default=False)
