from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for creating and editing books.
    """
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'isbn',
            'category',
            'description',
            'quantity',
            'available_quantity'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 13-digit ISBN'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Programming, Science, History'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief description of the book',
                'rows': 4
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Total copies'
            }),
            'available_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Available copies'
            }),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'isbn': 'ISBN',
            'category': 'Category',
            'description': 'Description',
            'quantity': 'Total Quantity',
            'available_quantity': 'Available Quantity',
        }
    
    def clean_isbn(self):
        """
        Validate ISBN format and uniqueness.
        """
        isbn = self.cleaned_data.get('isbn')
        
        # Check if ISBN is 13 characters
        if len(isbn) != 13:
            raise forms.ValidationError('ISBN must be exactly 13 characters.')
        
        # Check if ISBN contains only digits
        if not isbn.isdigit():
            raise forms.ValidationError('ISBN must contain only digits.')
        
        # Check uniqueness (only for new books, not when editing)
        if not self.instance.pk:  # Only check for new instances
            if Book.objects.filter(isbn=isbn).exists():
                raise forms.ValidationError('A book with this ISBN already exists.')
        
        return isbn
    
    def clean(self):
        """
        Validate that available_quantity doesn't exceed quantity.
        """
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        available_quantity = cleaned_data.get('available_quantity')
        
        if quantity and available_quantity:
            if available_quantity > quantity:
                raise forms.ValidationError(
                    'Available quantity cannot be greater than total quantity.'
                )
        
        return cleaned_data
