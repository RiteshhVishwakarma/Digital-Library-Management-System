from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Book


def book_list(request):
    """
    Display a list of all books with search functionality.
    """
    # Get search query from GET parameters
    search_query = request.GET.get('q', '').strip()
    
    # Start with all books
    books = Book.objects.all()
    
    # Apply search filter if query exists
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )
    
    context = {
        'books': books,
        'total_books': books.count(),
        'search_query': search_query,
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
