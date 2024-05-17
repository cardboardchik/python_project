from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

class CartListSerializer(serializers.ModelSerializer):
    item_descr = serializers.DictField()
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'is_active', 'user', 'item', 'cart', 'item_descr']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True, source='cartitem_set')

    class Meta:
        model = Cart
        fields = ['user', 'date_added', 'cart_items']