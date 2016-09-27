from django.shortcuts import render
from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from rest_framework import generics, response
from rest_framework.views import APIView

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

client = Elasticsearch()


class BooksList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request):
        user = self.request.user
        # request.data['author_id'] = user
        # print request.data
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = user
            print serializer.validated_data
            serializer.save()
            return response.Response(serializer.data)
        return response.Response({'data': 'Something went wrong!'})


class SearchBooks(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        params = self.request.query_params.get('query', None)
        print params
        search = Search(using=client, index=settings.ES_INDEX)

        query = Q('multi_match',
                  type='phrase_prefix',
                  query=params,
                  fields=['author.name', 'title'])
        search = search.query(query)
        search = search[:settings.ES_PAGINATION_SIZE]
        response = search.execute()
        return response
