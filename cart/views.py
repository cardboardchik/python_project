from rest_framework import generics, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, Cart
from .serializers import  CartItemSerializer, CartSerializer
from django.shortcuts import get_object_or_404
from django.core import serializers as ser
from django.db.models import Count
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.permissions import IsAuthenticated


class CartItemAPIView(viewsets.ViewSet):
   
    permission_classes = [IsAuthenticated]
    @extend_schema(request=inline_serializer(
        name="CartItem",
        fields={
            "quantity": serializers.IntegerField(),
            "is_active": serializers.BooleanField(),
            "item": serializers.IntegerField(),  
        },
    ), responses=CartItemSerializer)
    def create(self, request):
        """
        Request Body:<br>
            quantity: Integer (required)<br>
            is_active: Boolean (required)<br>
            item: Integer (required)<br>


        Example:
        {<br>
            "quantity": 1,<br>
            "is_active": true,<br>
            "item": 1,<br>
        }<br>

        If successful, returns the created cart item data. If quantity is less than or equal to 0, returns an error response. If the cart item already exists, updates the quantity and returns the updated data.
        """
        if not Cart.objects.filter(user=request.user.id):
            Cart.objects.create(user=request.user)
        cart = Cart.objects.get(user=request.user.id)

       

        cart_item = CartItem.objects.filter(cart=cart.id, user=request.user.id, item=request.data['item']).first()

        if cart_item:
            cart_item.quantity += int(request.data['quantity'])
            cart_item.save()
            
            data = CartItemSerializer(cart_item)
            return Response(data.data, status=status.HTTP_200_OK)
      
        if int(request.data['quantity']) <= 0:
            return Response({'error: quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        
        # serializer = CartItemSerializer(data=request.data | {'user': request.user.id, 'cart': cart.id})

        
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        cart_item = CartItem.objects.create(user=request.user, cart=cart, item_id=request.data['item'], quantity=request.data['quantity'], is_active=request.data['is_active'])
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(request=inline_serializer(
        name="CartItem_patch",
        fields={
            "quantity": serializers.IntegerField(),
        },
    ), responses=CartItemSerializer)
    def partial_update(self, request, pk=None):
        """
        PATCH /cart/items/{id}/: <br>

        Request Body:<br>
        quantity: Integer (required)<br>

        Example:<br>
        {<br>
            "quantity": 1<br>
        }<br>

        Update the cart item’s quantity and return the updated data. If the quantity is invalid (<= 0), return a 400 Bad Request response
        """
        if int(request.data['quantity']) <= 0:
            return Response({'error: quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = CartItem.objects.get(pk=pk)
        cart_item.quantity = request.data['quantity']
        cart_item.save()

        data = CartItemSerializer(CartItem.objects.get(pk=pk))
        return Response(data.data, status=status.HTTP_200_OK)
    
    
    def destroy(self, request, pk=None):
        """
        DELETE /cart/items/{id}/: <br>Delete the specified cart item.
        """
        CartItem.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)


class CartAPIView(viewsets.ViewSet):
    """
    Endpoints:
    - GET /cart/: Returns a list of cart items associated with the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = CartItem.objects.all()
        items = []
        for i in queryset:
            if i.user.id == request.user.id:
                items.append(i)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def destroy(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)
    



