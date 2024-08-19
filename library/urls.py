# attractive/urls.py

from django.contrib import admin
from django.urls import path
from books import views

urlpatterns = [
    path('', views.redirect_root),  # Redirect root URL to the book list
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('authors/', views.AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('favorites/', views.FavoriteBookList.as_view(), name='favorite-books'),
    path('recommendations/', views.RecommendationView.as_view(), name='recommendations'),
]
