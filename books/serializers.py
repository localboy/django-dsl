from rest_framework.serializers import ModelSerializer

from .models import Author, Book


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = (
            'id',
            'email',
            'name'
        )


class BookSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    class Meta:
        model = Book
        fields = (
            'author',
            'title',
            'description'
        )