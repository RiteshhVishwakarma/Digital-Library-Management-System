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
    User dashboard view.
    """
    return render(request, 'accounts/dashboard.html')


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
