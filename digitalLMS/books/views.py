from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book
from .forms import BookForm


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


@login_required
def add_book(request):
    """
    Create a new book.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(
                request,
                f'Book "{book.title}" has been added successfully!'
            )
            return redirect('books:book_list')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Book'
    }
    return render(request, 'books/add_book.html', context)


@login_required
def edit_book(request, pk):
    """
    Edit an existing book.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(
                request,
                f'Book "{book.title}" has been updated successfully!'
            )
            return redirect('books:book_detail', pk=book.pk)
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'page_title': 'Edit Book'
    }
    return render(request, 'books/edit_book.html', context)


@login_required
def delete_book(request, pk):
    """
    Delete a book with confirmation.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(
            request,
            f'Book "{book_title}" has been deleted successfully!'
        )
        return redirect('books:book_list')
    
    context = {
        'book': book
    }
    return render(request, 'books/delete_book.html', context)
