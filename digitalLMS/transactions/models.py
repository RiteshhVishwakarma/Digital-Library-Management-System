from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from books.models import Book


class BorrowTransaction(models.Model):
    """
    Model representing a book borrowing transaction.
    """
    STATUS_CHOICES = [
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
        ('Overdue', 'Overdue'),
    ]
    
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='borrow_transactions',
        help_text="Member who borrowed the book"
    )
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrow_transactions',
        help_text="Book that was borrowed"
    )
    
    issue_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the book was issued"
    )
    
    due_date = models.DateTimeField(
        help_text="Date and time when the book should be returned"
    )
    
    return_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when the book was actually returned"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Borrowed',
        help_text="Current status of the transaction"
    )
    
    class Meta:
        ordering = ['-issue_date']
        verbose_name = 'Borrow Transaction'
        verbose_name_plural = 'Borrow Transactions'
    
    def __str__(self):
        """
        String representation of the BorrowTransaction model.
        """
        return f"{self.member.username} - {self.book.title} ({self.status})"
    
    def save(self, *args, **kwargs):
        """
        Override save to automatically set due_date if not provided.
        """
        if not self.due_date:
            # Set due_date to 14 days after issue_date
            if self.issue_date:
                self.due_date = self.issue_date + timedelta(days=14)
            else:
                # If issue_date is not set yet, use current time + 14 days
                self.due_date = timezone.now() + timedelta(days=14)
        
        super().save(*args, **kwargs)
    
    def is_overdue(self):
        """
        Check if the transaction is overdue.
        """
        if self.status == 'Returned':
            return False
        return timezone.now() > self.due_date
    
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
    
    def days_until_due(self):
        """
        Calculate number of days until due date.
        """
        if self.status == 'Returned':
            return 0
        delta = self.due_date - timezone.now()
        return delta.days
    
    def days_overdue(self):
        """
        Calculate number of days overdue.
        """
        if self.status == 'Returned' or not self.is_overdue():
            return 0
        delta = timezone.now() - self.due_date
        return delta.days
