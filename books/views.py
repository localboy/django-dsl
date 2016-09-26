from django.shortcuts import render

from rest_framework import generics, response

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BooksList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request):
        user = self.request.user
        # request.data['author_id'] = user
        print request.data
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = user
            print serializer.validated_data
            serializer.save()
            return response.Response(serializer.data)
