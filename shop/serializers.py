from rest_framework import serializers
from .models import Product, Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'pk',
            'customer_surname',
            'customer_name',
            'customer_patronymic',
            'delivery_address',
            'delivery_type',
            'creation_date',
            'finish_date',
            'product',
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'creation_date',
            'image',
            'isActive',
            'category',
            'tag',
            'parameter',
        ]