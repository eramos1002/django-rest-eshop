from rest_framework import serializers
from .models import Person, Product, PurchasedItem


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'email', 'purchased_items']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'stock']


class PurchasedItemSerializer(serializers.ModelSerializer):
    personId = serializers.IntegerField(source='person.id', read_only=True)
    email = serializers.CharField(source='person.email', read_only=True)
    productId = serializers.IntegerField(source='product.id', read_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = PurchasedItem
        fields = ['personId', 'email', 'productId', 'quantity']

