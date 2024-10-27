from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'publication_date', 
                 'edition', 'summary', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_publication_date(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Publication date cannot be in the future")
        return value