from django.db import models
from django.contrib.auth.models import User
from projects.models import CompletedOrder


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
