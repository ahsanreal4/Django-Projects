from rest_framework import generics
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, UserSerializer, UserCreateSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager, IsManagerOrDeliveryCrew
from .constants import Constants
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from django.forms.models import model_to_dict
from datetime import date
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


"""
================================================    
================================================    
================================================    
    
    
                Menu Item Views 
    
    
================================================    
================================================    
================================================        
"""


class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields=['price','title']
    search_fields = ['title', 'category']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager]
        return [permission() for permission in permission_classes]
    
class MenuItemSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager]
        return [permission() for permission in permission_classes]
    
    
"""
================================================    
================================================    
================================================    
    
    
                Group Views 
    
    
================================================    
================================================    
================================================        
"""

class ManagerGroupListView(generics.ListCreateAPIView):
    group = Group.objects.get(name=Constants.MANAGER)
    queryset = User.objects.filter(groups=group)
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserCreateSerializer
        
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = request.data.get('username')
        user = User.objects.get(username=username)
        user.groups.add(self.group)
        user.save()
        return response

class ManagerGroupSingleView(generics.DestroyAPIView):
    group = Group.objects.get(name=Constants.MANAGER)
    queryset = User.objects.filter(groups=group)
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
class DeliveryCrewGroupListView(generics.ListCreateAPIView):
    group = Group.objects.get(name=Constants.DELIVERY_CREW)
    queryset = User.objects.filter(groups=group)
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserCreateSerializer
        
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = request.data.get('username')
        user = User.objects.get(username=username)
        user.groups.add(self.group)
        user.save()
        return response

class DeliveryCrewGroupSingleView(generics.DestroyAPIView):
    group = Group.objects.get(name=Constants.DELIVERY_CREW)
    queryset = User.objects.filter(groups=group)
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


"""
================================================    
================================================    
================================================    
    
    
                Cart Views 
    
    
================================================    
================================================    
================================================        
"""

class CartListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
            
    def get_queryset(self):
        user_id = self.request.user.id
        query_set = Cart.objects.filter(user=user_id)
        return query_set
    
    def create(self, request, *args, **kwargs):
        menu_item_id = request.data.get("menuitem")
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        
        quantity = request.data.get('quantity')
        unit_price = float(menu_item.price)
        price = float(unit_price * quantity)
        
        request.data['unit_price'] = unit_price
        request.data['user'] = request.user.id
        request.data['price'] = price
                
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        query_set.delete()
        
        return Response(status=HTTP_204_NO_CONTENT)
    
    
"""
================================================    
================================================    
================================================    
    
    
                Order Item Views 
    
    
================================================    
================================================    
================================================        
"""

class OrderListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    ordering_fields=['date','total']
    search_fields = ['status']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_queryset(self):
        user_id = self.request.user.id
        groups = self.request.user.groups 
        
        # Manager
        if groups.filter(name=Constants.MANAGER).exists():
            query_set = Order.objects.all()
        # Delivery Crew    
        elif groups.filter(name=Constants.DELIVERY_CREW).exists():
            query_set = Order.objects.filter(delivery_crew=user_id)
        # Customer
        else: 
            query_set = Order.objects.filter(user=user_id)
        return query_set
    
    def list(self, request, *args, **kwargs):
        
        orders = self.get_queryset()
        
        data = []
        
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            order_items_list = [model_to_dict(order_item) for order_item in order_items]
            
            order_dict = model_to_dict(order)
            order_dict['order_items'] = order_items_list
            
            data.append(order_dict)

        return Response(data=data, status=HTTP_200_OK)
    
    
    def create(self, request, *args, **kwargs):
        body = request.data
        
        user_id = request.user.id
        
        # Get all cart items
        cart_items = Cart.objects.filter(user=user_id)

        # In case of no items in cart we don't create an order
        if len(cart_items) == 0:
            return Response({"detail": "No items found in cart"}, status=HTTP_400_BAD_REQUEST)

        total_price = 0
        
        for item in cart_items:
            total_price += item.price
            
        body['total'] = total_price
        body['user'] = user_id
        body['date'] = date.today()
        
        # Create Order
        order_serializer = OrderSerializer(data=body)
        order_serializer.is_valid(raise_exception=True)
        order: Order = order_serializer.save()
        
        
        # Create Order Items
        for item in cart_items:
            order_item_dict = {
                'order': order.id,
                'menuitem': item.menuitem.id,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'price': item.price
            }
            order_item_serializer = OrderItemSerializer(data=order_item_dict)
            order_item_serializer.is_valid(raise_exception=True)
            order_item_serializer.save()
        
        # Delete Cart Items
        cart_items.delete()
        
        return Response(status=HTTP_201_CREATED)
    
    
class OrderSingleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        method = self.request.method
        
        if method == 'GET':
            permission_classes = [IsAuthenticated]
        elif method == 'PATCH':
            permission_classes = [IsAuthenticated, IsManagerOrDeliveryCrew]
        else:
            permission_classes = [IsAuthenticated, IsManager]
            
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user_id = self.request.user.id
        groups = self.request.user.groups 
        
        # Manager
        if groups.filter(name=Constants.MANAGER).exists():
            query_set = Order.objects.all()
        # Delivery Crew    
        elif groups.filter(name=Constants.DELIVERY_CREW).exists():
            query_set = Order.objects.filter(delivery_crew=user_id)
        # Customer
        else: 
            query_set = Order.objects.filter(user=user_id)
        return query_set        
            
    def update(self, request, *args, **kwargs):
        body = request.data
        data_length = len(body.keys())
        groups = self.request.user.groups 
        
        status = body.get('status')
        
        if data_length > 1 or status is None:
            if not groups.filter(name=Constants.MANAGER).exists():
                return Response(status=HTTP_403_FORBIDDEN, data={"detail": "You are not authorized to update this data"})
              
        return super().update(request, *args, **kwargs)