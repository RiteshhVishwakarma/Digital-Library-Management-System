from django.shortcuts import render, redirect
from django.contrib.auth import login, logout


def register(request):
    """
    Handle user registration.
    """
    return render(request, 'accounts/register.html')


def login_view(request):
    """
    Handle user login.
    """
    return render(request, 'accounts/login.html')


def logout_view(request):
    """
    Handle user logout.
    """
    pass
