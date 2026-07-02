from django.db import models


class Category(models.Model):
    """
    Model representing a book category.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Enter the category name (e.g., Programming, Fiction)"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Enter a brief description of this category"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the category was created"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        """
        String representation of the Category model.
        """
        return self.name
    
    def book_count(self):
        """
        Return the number of books in this category.
        """
        return self.books.count()
    
    book_count.short_description = 'Number of Books'


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
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='books',
        help_text="Select the book category"
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
