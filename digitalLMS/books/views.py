from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book, Category
from .forms import BookForm
from accounts.decorators import librarian_required


def book_list(request):
    """
    Display a list of all books with search and category filter functionality.
    Accessible to all users (including non-authenticated).
    """
    # Get search query and category filter from GET parameters
    search_query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    
    # Start with all books
    books = Book.objects.select_related('category').all()
    
    # Apply search filter if query exists
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    
    # Apply category filter if selected
    if category_filter:
        books = books.filter(category__id=category_filter)
    
    # Get all categories for the filter dropdown
    categories = Category.objects.all()
    
    context = {
        'books': books,
        'categories': categories,
        'total_books': books.count(),
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'books/book_list.html', context)


def book_detail(request, pk):
    """
    Display details of a specific book.
    Accessible to all users (including non-authenticated).
    """
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book
    }
    return render(request, 'books/book_detail.html', context)


@librarian_required
def add_book(request):
    """
    Create a new book.
    Only accessible to librarians.
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


@librarian_required
def edit_book(request, pk):
    """
    Edit an existing book.
    Only accessible to librarians.
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


@librarian_required
def delete_book(request, pk):
    """
    Delete a book with confirmation.
    Only accessible to librarians.
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
