from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm


def home(request):
    """
    Home page view.
    """
    return render(request, 'accounts/home.html')


@login_required
def dashboard(request):
    """
    User dashboard view with real statistics.
    """
    from transactions.models import BorrowTransaction
    
    # Get user's borrow statistics
    if request.user.profile.is_member():
        # Member statistics
        total_borrowed = BorrowTransaction.objects.filter(member=request.user).count()
        active_loans = BorrowTransaction.objects.filter(
            member=request.user,
            status='Borrowed'
        ).count()
        overdue_books = BorrowTransaction.objects.filter(
            member=request.user,
            status='Overdue'
        ).count()
        returned_books = BorrowTransaction.objects.filter(
            member=request.user,
            status='Returned'
        ).count()
        
        # Get recent borrowed books (latest 5)
        recent_transactions = BorrowTransaction.objects.filter(
            member=request.user
        ).select_related('book').order_by('-issue_date')[:5]
        
        context = {
            'total_borrowed': total_borrowed,
            'active_loans': active_loans,
            'overdue_books': overdue_books,
            'returned_books': returned_books,
            'recent_transactions': recent_transactions,
        }
    else:
        # Librarian statistics
        total_transactions = BorrowTransaction.objects.count()
        active_borrows = BorrowTransaction.objects.filter(status='Borrowed').count()
        overdue_count = BorrowTransaction.objects.filter(status='Overdue').count()
        total_returned = BorrowTransaction.objects.filter(status='Returned').count()
        
        context = {
            'total_transactions': total_transactions,
            'active_borrows': active_borrows,
            'overdue_count': overdue_count,
            'total_returned': total_returned,
        }
    
    return render(request, 'accounts/dashboard.html', context)


def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Save the user
                user = form.save()
                messages.success(request, f'Account created successfully for {user.username}! You can now login.')
                return redirect('accounts:login')
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    """
    # Redirect if user is already authenticated
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next parameter or dashboard
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('accounts:dashboard')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Handle user logout.
    """
    username = request.user.username
    logout(request)
    messages.success(request, f'You have been logged out successfully, {username}!')
    return redirect('accounts:home')


@login_required
def my_borrowed_books(request):
    """
    Display all borrowed books for the logged-in member.
    """
    from transactions.models import BorrowTransaction
    
    # Only accessible to members
    if not request.user.profile.is_member():
        messages.error(request, 'This page is only accessible to members.')
        return redirect('accounts:dashboard')
    
    # Get all transactions for the current user
    all_transactions = BorrowTransaction.objects.filter(
        member=request.user
    ).select_related('book').order_by('-issue_date')
    
    # Separate by status
    borrowed_books = all_transactions.filter(status__in=['Borrowed', 'Overdue'])
    returned_books = all_transactions.filter(status='Returned')
    
    context = {
        'borrowed_books': borrowed_books,
        'returned_books': returned_books,
        'borrowed_count': borrowed_books.count(),
        'returned_count': returned_books.count(),
    }
    
    return render(request, 'accounts/my_borrowed_books.html', context)
