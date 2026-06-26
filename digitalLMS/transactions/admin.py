from django.contrib import admin
from .models import BorrowTransaction


@admin.register(BorrowTransaction)
class BorrowTransactionAdmin(admin.ModelAdmin):
    """
    Admin configuration for BorrowTransaction model.
    """
    list_display = [
        'id',
        'member',
        'book',
        'issue_date',
        'due_date',
        'return_date',
        'status',
        'is_overdue'
    ]
    
    list_filter = [
        'status',
        'issue_date',
        'due_date',
        'return_date'
    ]
    
    search_fields = [
        'member__username',
        'member__email',
        'book__title',
        'book__author',
        'book__isbn'
    ]
    
    readonly_fields = [
        'issue_date',
        'is_overdue',
        'days_until_due',
        'days_overdue'
    ]
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('member', 'book', 'status')
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date', 'return_date')
        }),
        ('Status Information', {
            'fields': ('is_overdue', 'days_until_due', 'days_overdue')
        }),
    )
    
    ordering = ['-issue_date']
    
    list_per_page = 25
    
    date_hierarchy = 'issue_date'
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related to reduce database queries.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('member', 'book')
