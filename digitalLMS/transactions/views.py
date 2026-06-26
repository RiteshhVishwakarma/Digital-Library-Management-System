from django.shortcuts import render, redirect
from django.contrib import messages
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
    Display list of all borrow transactions.
    Only accessible to librarians.
    """
    transactions = BorrowTransaction.objects.select_related(
        'member', 'member__profile', 'book'
    ).all()
    
    # Update overdue status
    for trans in transactions:
        if trans.status == 'Borrowed' and trans.is_overdue():
            trans.status = 'Overdue'
            trans.save()
    
    context = {
        'transactions': transactions,
        'total_transactions': transactions.count(),
        'active_borrows': transactions.filter(status='Borrowed').count(),
        'overdue_count': transactions.filter(status='Overdue').count(),
        'page_title': 'Transaction History'
    }
    return render(request, 'transactions/transaction_list.html', context)
