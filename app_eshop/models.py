import uuid

from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()


class PurchasedItem(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='purchased_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()