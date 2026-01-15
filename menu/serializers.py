from rest_framework import serializers
from .models import MenuItem,Category
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.contrib.auth import authenticate
from django.utils import timezone
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    title=serializers.CharField()
    slug=serializers.CharField
    
    class Meta:
        model=Category
        fields=['id','title','slug']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    featured = serializers.BooleanField()
    price_after_tax = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['title','featured','category','price','inventory','price_after_tax']

    def get_price_after_tax(self, obj):
        tax_rate = Decimal(0.16)
        return round(obj.price + (obj.price * tax_rate), 2)

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(**category_data)
        menu_item = MenuItem.objects.create(category=category, **validated_data)
        return menu_item
