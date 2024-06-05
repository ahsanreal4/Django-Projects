from django.urls import path
from .views import ListBookView, SingleBookView

urlpatterns = [
    path('books', ListBookView.as_view(),  name='books'),
    path('books/<int:pk>', SingleBookView.as_view(), name='books_single')
]
