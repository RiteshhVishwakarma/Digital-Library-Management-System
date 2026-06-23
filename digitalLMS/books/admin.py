from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model.
    """
    list_display = [
        'title',
        'author',
        'isbn',
        'category',
        'quantity',
        'available_quantity',
        'is_available',
        'created_at'
    ]
    
    list_filter = [
        'category',
        'created_at',
    ]
    
    search_fields = [
        'title',
        'author',
        'isbn',
        'category'
    ]
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'isbn', 'category')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Inventory', {
            'fields': ('quantity', 'available_quantity')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
    
    ordering = ['-created_at']
    
    list_per_page = 25
