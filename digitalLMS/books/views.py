from django.shortcuts import render, get_object_or_404
from .models import Book


def book_list(request):
    """
    Display a list of all books.
    """
    books = Book.objects.all()
    context = {
        'books': books,
        'total_books': books.count()
    }
    return render(request, 'books/book_list.html', context)


def book_detail(request, pk):
    """
    Display details of a specific book.
    """
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book
    }
    return render(request, 'books/book_detail.html', context)
