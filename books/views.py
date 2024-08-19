# books/views.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Author, FavoriteBook
from .serializers import BookSerializer, AuthorSerializer, FavoriteBookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect


def redirect_root(request):
    return redirect('book-list')

# Books API
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            return Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
        return super().get_queryset()

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Authors API
class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# User Registration and Authentication
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

# Favorites and Recommendations API
class FavoriteBookList(generics.ListCreateAPIView):
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteBook.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if FavoriteBook.objects.filter(user=self.request.user).count() >= 20:
            return Response({"error": "Maximum 20 favorite books allowed."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)

class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_favorites = FavoriteBook.objects.filter(user=request.user).values_list('book__id', flat=True)
        recommendations = Book.objects.exclude(id__in=user_favorites).order_by('?')[:5]  # Random 5 books not in favorites
        serializer = BookSerializer(recommendations, many=True)
        return Response(serializer.data)
