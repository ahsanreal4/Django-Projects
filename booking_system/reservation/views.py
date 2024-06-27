from django.shortcuts import render

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models

def index(request):
    return render(request, 'index.html')

# Create your views here.
class MenuItemView(generics.ListCreateAPIView):
    serializer_class = serializers.MenuSerializer
    queryset = models.Menu.objects.all()
    permission_classes = [IsAuthenticated]
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = models.Menu.objects.all()
    serializer_class = serializers.MenuSerializer
    permission_classes = [IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer
    permission_classes = [IsAuthenticated]