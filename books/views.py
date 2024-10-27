from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import Book
from .serializers import BookSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @swagger_auto_schema(
        operation_description="List all books with pagination",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('per_page', openapi.IN_QUERY, description="Items per page", type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request):
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))
        
        paginator = Paginator(self.queryset, per_page)
        total_pages = paginator.num_pages
        
        try:
            books = paginator.page(page)
        except:
            return Response({
                'status': 'error',
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Page not found',
                'errors': {
                    'detail': f'Page {page} does not exist. Total pages: {total_pages}'
                }
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(books, many=True)
        
        return Response({
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Books retrieved successfully',
            'data': {
                'books': serializer.data,
                'pagination': {
                    'current_page': page,
                    'per_page': per_page,
                    'total_pages': total_pages,
                    'total_books': paginator.count
                }
            },
            'links': {
                'self': f'/api/v1/books?page={page}',
                'next': f'/api/v1/books?page={page + 1}' if books.has_next() else None,
                'prev': f'/api/v1/books?page={page - 1}' if books.has_previous() else None
            }
        })

    @swagger_auto_schema(operation_description="Retrieve a specific book by ID")
    def retrieve(self, request, pk=None):
        try:
            book = self.get_object()
            serializer = self.serializer_class(book)
            return Response({
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Book retrieved successfully',
                'data': {
                    'book': serializer.data
                }
            })
        except:
            return Response({
                'status': 'error',
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Book not found',
                'errors': {
                    'detail': f'Book with ID {pk} does not exist'
                }
            }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_description="Create a new book")
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'code': status.HTTP_201_CREATED,
                'message': 'Book created successfully',
                'data': {
                    'book': serializer.data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Invalid data provided',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Update a book's details")
    def update(self, request, pk=None):
        try:
            book = self.get_object()
            serializer = self.serializer_class(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Book updated successfully',
                    'data': {
                        'book': serializer.data
                    }
                })
            return Response({
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'status': 'error',
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Book not found',
                'errors': {
                    'detail': f'Book with ID {pk} does not exist'
                }
            }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_description="Delete a book")
    def destroy(self, request, pk=None):
        try:
            book = self.get_object()
            book.delete()
            return Response({
                'status': 'success',
                'code': status.HTTP_204_NO_CONTENT,
                'message': 'Book deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'status': 'error',
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Book not found',
                'errors': {
                    'detail': f'Book with ID {pk} does not exist'
                }
            }, status=status.HTTP_404_NOT_FOUND)
