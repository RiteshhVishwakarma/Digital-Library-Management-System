from django import forms
from django.contrib.auth.models import User
from books.models import Book


class IssueBookForm(forms.Form):
    """
    Form for issuing books to members.
    """
    member = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='Member').select_related('profile'),
        empty_label="Select a member",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'member-select'
        }),
        help_text="Select the member who wants to borrow the book"
    )
    
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(available_quantity__gt=0),
        empty_label="Select a book",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'book-select'
        }),
        help_text="Select the book to issue"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom label display for members
        self.fields['member'].label_from_instance = lambda obj: f"{obj.username} - {obj.email}"
        # Custom label display for books
        self.fields['book'].label_from_instance = lambda obj: f"{obj.title} by {obj.author} (Available: {obj.available_quantity})"
