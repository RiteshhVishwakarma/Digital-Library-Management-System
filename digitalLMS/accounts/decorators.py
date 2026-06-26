from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps


def librarian_required(view_func):
    """
    Decorator to restrict access to librarian users only.
    Usage: @librarian_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('accounts:login')
        
        # Check if user has a profile
        if not hasattr(request.user, 'profile'):
            messages.error(request, 'Your account profile is not set up properly. Please contact support.')
            return redirect('accounts:dashboard')
        
        # Check if user is a librarian
        if not request.user.profile.is_librarian():
            messages.error(
                request,
                'Access Denied! This page is only accessible to librarians.'
            )
            return redirect('accounts:dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def member_required(view_func):
    """
    Decorator to restrict access to member users only.
    Usage: @member_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('accounts:login')
        
        # Check if user has a profile
        if not hasattr(request.user, 'profile'):
            messages.error(request, 'Your account profile is not set up properly. Please contact support.')
            return redirect('accounts:dashboard')
        
        # Check if user is a member
        if not request.user.profile.is_member():
            messages.error(
                request,
                'Access Denied! This page is only accessible to members.'
            )
            return redirect('accounts:dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def role_required(*roles):
    """
    Decorator to restrict access to users with specific roles.
    Usage: @role_required('Member', 'Librarian')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to access this page.')
                return redirect('accounts:login')
            
            # Check if user has a profile
            if not hasattr(request.user, 'profile'):
                messages.error(request, 'Your account profile is not set up properly. Please contact support.')
                return redirect('accounts:dashboard')
            
            # Check if user's role is in allowed roles
            if request.user.profile.role not in roles:
                messages.error(
                    request,
                    f'Access Denied! This page is only accessible to {", ".join(roles)}.'
                )
                return redirect('accounts:dashboard')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator
