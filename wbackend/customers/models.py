from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    user = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Membership(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    name = models.CharField(max_length=255)


class Subscription(models.Model):
    customer = models.ForeignKey(Customer)
    membership = models.ForeignKey(Membership)
