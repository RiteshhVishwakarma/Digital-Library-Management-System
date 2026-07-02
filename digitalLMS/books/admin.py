from django.contrib import admin
from .models import Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    """
    list_display = [
        'name',
        'description',
        'book_count',
        'created_at'
    ]
    
    search_fields = [
        'name',
        'description'
    ]
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
    
    ordering = ['name']
    
    list_per_page = 25


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
