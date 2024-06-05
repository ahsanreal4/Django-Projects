from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class BookView(viewsets.ViewSet):
    def list(self, request):
        return Response({"message":"All books"}, status.HTTP_200_OK)
    
    def create(self, request):
        return Response({"message":"Creating a book"}, status.HTTP_201_CREATED)
	
    def update(self, request, pk=None):
        return Response({"message":"Updating a book"}, status.HTTP_200_OK)
	
    def retrieve(self, request, pk=None):
        return Response({"message":"Displaying a book"}, status.HTTP_200_OK)
	
    def partial_update(self, request, pk=None):
        return Response({"message":"Partially updating a book"}, status.HTTP_200_OK)
	
    def destroy(self, request, pk=None):
        return Response({"message":"Deleting a book"}, status.HTTP_200_OK)
