from django.urls import path
from . import views
from .views import (BooksList, BookDetailView,
                    AuthorsListView,
                    AuthorDetailView,
                    LoanedBooksByUserListView,
                    AllLoanedBooksListView,
                    CreateAuthor,
                    UpdateAuthor,
                    CreateBook,
                    UpdateBook
                    )

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', BooksList.as_view(), name='catalog-books'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorsListView.as_view(), name='catalog-authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', AllLoanedBooksListView.as_view(), name='all-loaned-books'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', CreateAuthor.as_view(), name='create-author'),
    path('author/<int:pk>/edit/', UpdateAuthor.as_view(), name='update-author'),
    path('book/create/', CreateBook.as_view(), name='create-book'),
    path('book/<int:pk>/edit/', UpdateBook.as_view(), name='update-book'),
    ]