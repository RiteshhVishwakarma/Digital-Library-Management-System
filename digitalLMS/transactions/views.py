from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from accounts.decorators import librarian_required
from .forms import IssueBookForm
from .models import BorrowTransaction


@librarian_required
def issue_book(request):
    """
    Issue book page for librarians.
    Creates a BorrowTransaction and updates book inventory.
    """
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            book = form.cleaned_data['book']
            
            # Validation 1: Check if book is available
            if book.available_quantity <= 0:
                messages.error(
                    request,
                    f'Cannot issue "{book.title}". No copies are currently available.'
                )
                return render(request, 'transactions/issue_book.html', {
                    'form': form,
                    'page_title': 'Issue Book'
                })
            
            # Validation 2: Check if member already has this book borrowed
            existing_borrow = BorrowTransaction.objects.filter(
                member=member,
                book=book,
                status='Borrowed'
            ).exists()
            
            if existing_borrow:
                messages.error(
                    request,
                    f'{member.username} has already borrowed "{book.title}" and has not returned it yet.'
                )
                return render(request, 'transactions/issue_book.html', {
                    'form': form,
                    'page_title': 'Issue Book'
                })
            
            # Use database transaction to ensure data integrity
            try:
                with transaction.atomic():
                    # Create BorrowTransaction
                    borrow_transaction = BorrowTransaction.objects.create(
                        member=member,
                        book=book,
                        status='Borrowed'
                    )
                    
                    # Update book inventory
                    book.available_quantity -= 1
                    book.save()
                    
                    messages.success(
                        request,
                        f'Successfully issued "{book.title}" to {member.username}. '
                        f'Due date: {borrow_transaction.due_date.strftime("%B %d, %Y")}'
                    )
                    return redirect('transactions:transaction_list')
                    
            except Exception as e:
                messages.error(
                    request,
                    f'An error occurred while issuing the book: {str(e)}'
                )
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = IssueBookForm()
    
    context = {
        'form': form,
        'page_title': 'Issue Book'
    }
    return render(request, 'transactions/issue_book.html', context)


@librarian_required
def transaction_list(request):
    """
    Display list of all borrow transactions with search and filter functionality.
    Only accessible to librarians.
    """
    # Get search query and filter parameters from GET request
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'All').strip()
    
    # Start with all transactions
    transactions = BorrowTransaction.objects.select_related(
        'member', 'member__profile', 'book'
    ).all()
    
    # Update overdue status for all borrowed transactions
    for trans in transactions:
        if trans.status == 'Borrowed' and trans.is_overdue():
            trans.status = 'Overdue'
            trans.save()
    
    # Apply search filter if query exists
    if search_query:
        from django.db.models import Q
        transactions = transactions.filter(
            Q(member__username__icontains=search_query) |
            Q(book__title__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter and status_filter != 'All':
        transactions = transactions.filter(status=status_filter)
    
    # Calculate statistics (before filtering, use all transactions)
    all_transactions = BorrowTransaction.objects.all()
    
    context = {
        'transactions': transactions,
        'total_transactions': all_transactions.count(),
        'active_borrows': all_transactions.filter(status='Borrowed').count(),
        'overdue_count': all_transactions.filter(status='Overdue').count(),
        'filtered_count': transactions.count(),
        'search_query': search_query,
        'status_filter': status_filter,
        'page_title': 'Transaction History'
    }
    return render(request, 'transactions/transaction_list.html', context)


@librarian_required
def transaction_detail(request, pk):
    """
    Display detailed information about a specific transaction.
    Only accessible to librarians.
    """
    transaction_obj = get_object_or_404(
        BorrowTransaction.objects.select_related(
            'member', 'member__profile', 'book'
        ),
        pk=pk
    )
    
    # Update overdue status if needed
    if transaction_obj.status == 'Borrowed' and transaction_obj.is_overdue():
        transaction_obj.status = 'Overdue'
        transaction_obj.save()
    
    context = {
        'transaction': transaction_obj,
        'page_title': f'Transaction #{transaction_obj.id}'
    }
    return render(request, 'transactions/transaction_detail.html', context)


@librarian_required
def return_book(request, pk):
    """
    Return a borrowed book with confirmation.
    Only accessible to librarians.
    """
    transaction_obj = get_object_or_404(
        BorrowTransaction.objects.select_related(
            'member', 'member__profile', 'book'
        ),
        pk=pk
    )
    
    # Validation: Check if already returned
    if transaction_obj.status == 'Returned':
        messages.error(
            request,
            f'This book has already been returned on {transaction_obj.return_date.strftime("%B %d, %Y")}.'
        )
        return redirect('transactions:transaction_detail', pk=pk)
    
    if request.method == 'POST':
        # Process the return
        try:
            with transaction.atomic():
                # Set return date to current time
                transaction_obj.return_date = timezone.now()
                transaction_obj.status = 'Returned'
                transaction_obj.save()
                
                # Increase book's available quantity
                book = transaction_obj.book
                book.available_quantity += 1
                book.save()
                
                messages.success(
                    request,
                    f'Successfully returned "{book.title}". '
                    f'Available quantity updated to {book.available_quantity}/{book.quantity}.'
                )
                return redirect('transactions:transaction_list')
                
        except Exception as e:
            messages.error(
                request,
                f'An error occurred while processing the return: {str(e)}'
            )
            return redirect('transactions:transaction_detail', pk=pk)
    
    # GET request - show confirmation page
    context = {
        'transaction': transaction_obj,
        'page_title': 'Return Book Confirmation'
    }
    return render(request, 'transactions/return_book.html', context)


@login_required
def borrow_book(request, book_id):
    """
    Allow members to borrow books (self-service).
    Shows confirmation page before borrowing.
    """
    from books.models import Book
    from accounts.decorators import member_required
    
    # Check if user is a member
    if not request.user.profile.is_member():
        messages.error(
            request,
            'Only members can borrow books. Librarians should use the Issue Book feature.'
        )
        return redirect('books:book_detail', pk=book_id)
    
    book = get_object_or_404(Book, pk=book_id)
    
    # Validation 1: Check if book is available
    if book.available_quantity <= 0:
        messages.error(
            request,
            f'Sorry, "{book.title}" is currently unavailable. All copies are borrowed.'
        )
        return redirect('books:book_detail', pk=book_id)
    
    # Validation 2: Check if member already has this book borrowed
    existing_borrow = BorrowTransaction.objects.filter(
        member=request.user,
        book=book,
        status__in=['Borrowed', 'Overdue']
    ).exists()
    
    if existing_borrow:
        messages.error(
            request,
            f'You have already borrowed "{book.title}" and have not returned it yet.'
        )
        return redirect('books:book_detail', pk=book_id)
    
    if request.method == 'POST':
        # Process the borrow request
        try:
            with transaction.atomic():
                # Create BorrowTransaction
                borrow_transaction = BorrowTransaction.objects.create(
                    member=request.user,
                    book=book,
                    status='Borrowed'
                )
                
                # Update book inventory
                book.available_quantity -= 1
                book.save()
                
                messages.success(
                    request,
                    f'Successfully borrowed "{book.title}"! '
                    f'Please return it by {borrow_transaction.due_date.strftime("%B %d, %Y")}.'
                )
                return redirect('accounts:dashboard')
                
        except Exception as e:
            messages.error(
                request,
                f'An error occurred while processing your request: {str(e)}'
            )
            return redirect('books:book_detail', pk=book_id)
    
    # GET request - show confirmation page
    context = {
        'book': book,
        'page_title': 'Confirm Book Borrow'
    }
    return render(request, 'transactions/borrow_book.html', context)
