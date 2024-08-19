# books/serializers.py

from rest_framework import serializers
from .models import Book, Author, FavoriteBook

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class FavoriteBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = FavoriteBook
        fields = ['book']
