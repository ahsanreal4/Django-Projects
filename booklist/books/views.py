from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class ListBookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    ordering_fields=['price', 'title', 'author']
    search_fields=['title', 'author']

class SingleBookView(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
