from django.db import models


class Book(models.Model):
    """
    Model representing a book in the library.
    """
    title = models.CharField(
        max_length=200,
        help_text="Enter the book title"
    )
    
    author = models.CharField(
        max_length=100,
        help_text="Enter the author name"
    )
    
    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text="13 Character ISBN number"
    )
    
    category = models.CharField(
        max_length=50,
        help_text="Enter the book category (e.g., Fiction, Science, History)"
    )
    
    description = models.TextField(
        help_text="Enter a brief description of the book",
        blank=True
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Total number of copies in the library"
    )
    
    available_quantity = models.PositiveIntegerField(
        default=1,
        help_text="Number of copies currently available for borrowing"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the book was added to the system"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
    
    def __str__(self):
        """
        String representation of the Book model.
        """
        return f"{self.title} by {self.author}"
    
    def is_available(self):
        """
        Check if the book is available for borrowing.
        """
        return self.available_quantity > 0
    
    is_available.boolean = True
    is_available.short_description = 'Available'
