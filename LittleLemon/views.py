from django.shortcuts import get_object_or_404
from .serializers import (
    OrderSerializer,
    CartSerializer
)
from LittleLemon.models import Cart, Order, OrderItem
from rest_framework import generics, permissions, status, filters,viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from accounts.views import IsManager,IsDeliveryCrew
from menu.models import MenuItem
from django.contrib.auth.models import User
    
            

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user
   
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method=='POST':
        menu_item_title = request.data.get('menu_item_title')
        quantity_raw = int(request.data.get('quantity',1))  

        quantity = (quantity_raw)
        
      
        if not menu_item_title or not quantity_raw:
            return Response({'message':'menu_item_title and quantity are required'})
        
        menu_item = get_object_or_404(MenuItem, title__iexact=menu_item_title)
        unit_price = menu_item.price
        price = unit_price * quantity

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            menu_item=menu_item,
            defaults={
                'unit_price': unit_price,
                'quantity': quantity,
                'price': price
            }
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.price = cart_item.unit_price * cart_item.quantity
            cart_item.save()

        serializer = CartSerializer(cart_item)

        return Response(
            {
                'message': 'Item added to cart',
                'item': serializer.data
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user=self.request.user
        
        if user.groups.filter(name='manager').exists() or user.is_staff:
            return Order.objects.all()
        elif user.groups.filter(name='delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=True, methods=['post'], permission_classes=[IsManager])
    def assing_delivery(self,request,pk=None):
        order = self.get_object()
        crew_id=request.data.get('crew_id')
        
        if not crew_id:
            return Response({'message':'error crew_id is required'},status.HTTP_400_BAD_REQUEST)
        
        try:
            crew_member=User.objects.get(id=crew_id)
        except User.DoesNotExist:
            return Response({'message':'user does not exist'},status.HTTP_400_BAD_REQUEST)
        
        
        order.delivery_crew=crew_member
        order.save()
        
        return Response({'message':f'order{order.id} assingm=ned to crew member{crew_id}'},status.HTTP_200_OK)
    
     
    @action(detail=True, methods=['POST'], permission_classes=[IsManager])
    def mark_delivered(self,request,pk=None):
        order = self.request.object()
        if Order.delivery_crew != request.user:
             return Response({'message':'error you were not assinged his order'},status.HTTP_400_BAD_REQUEST)
         
        order.status= True
        order.save()
        
        return Response({'message':f'{order.id}has been delivered','order':OrderSerializer(order).data},status.HTTP_200_OK)
         
  