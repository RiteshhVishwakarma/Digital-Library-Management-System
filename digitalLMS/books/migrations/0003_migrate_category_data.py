# Data migration for converting category strings to Category objects
from django.db import migrations


def migrate_categories_forward(apps, schema_editor):
    """
    Convert old category strings to Category objects.
    """
    Book = apps.get_model('books', 'Book')
    Category = apps.get_model('books', 'Category')
    
    # Get all unique category strings from books
    books = Book.objects.all()
    
    if not books.exists():
        # No books to migrate
        return
    
    # Create categories from existing book categories
    for book in books:
        if book.category_old:
            # Get or create category
            category, created = Category.objects.get_or_create(
                name=book.category_old.strip(),
                defaults={'description': f'Books related to {book.category_old}'}
            )
            # Link book to category
            book.category_new = category
            book.save()


def migrate_categories_backward(apps, schema_editor):
    """
    Convert Category objects back to strings.
    """
    Book = apps.get_model('books', 'Book')
    
    for book in Book.objects.all():
        if book.category_new:
            book.category_old = book.category_new.name
            book.save()


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_create_category_model'),
    ]

    operations = [
        migrations.RunPython(
            migrate_categories_forward,
            migrate_categories_backward
        ),
    ]
