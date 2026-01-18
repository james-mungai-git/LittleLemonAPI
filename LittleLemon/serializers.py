from rest_framework import serializers
from .models import OrderItem,Order,Cart
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.contrib.auth import authenticate
from django.utils import timezone
from decimal import Decimal



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['user', 'status', 'delivery_crew', 'date', 'total']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            raise serializers.ValidationError("Cannot place order. Cart is empty.")

        total = sum(item.price for item in cart_items)

        order = Order.objects.create(
            user=user,
            status=False,
            total=total,
            date=timezone.now().date()
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )

        cart_items.delete()

        return order

class CartSerializer(serializers.ModelSerializer):
    menu_item = serializers.StringRelatedField()  
    user = serializers.StringRelatedField()       

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menu_item', 'quantity', 'unit_price', 'price']
