from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    """
    Django management command to clear all books from the database.
    Usage: python manage.py clear_books
    WARNING: This will delete all book records!
    """
    help = 'Deletes all books from the database (development only)'

    def add_arguments(self, parser):
        """
        Add optional arguments to the command.
        """
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **kwargs):
        """
        Main command logic to delete all books.
        """
        no_input = kwargs.get('no_input')
        
        # Get current book count
        book_count = Book.objects.count()
        
        if book_count == 0:
            self.stdout.write(self.style.WARNING('⚠ No books found in the database.'))
            return
        
        self.stdout.write(self.style.WARNING(f'\n⚠ WARNING: This will delete {book_count} book(s) from the database!'))
        
        # Confirmation prompt (unless --no-input flag is used)
        if not no_input:
            self.stdout.write(self.style.WARNING('This action cannot be undone.\n'))
            confirm = input('Are you sure you want to continue? Type "yes" to confirm: ')
            
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('✗ Operation cancelled.'))
                return
        
        # Delete all books
        self.stdout.write('\nDeleting books...')
        deleted_books = []
        
        for book in Book.objects.all():
            deleted_books.append(f'"{book.title}" by {book.author}')
        
        deleted_count, _ = Book.objects.all().delete()
        
        # Print deleted books
        for book_info in deleted_books:
            self.stdout.write(self.style.ERROR(f'✗ Deleted: {book_info}'))
        
        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ All books cleared from database!'))
        self.stdout.write(self.style.SUCCESS(f'  - Total books deleted: {deleted_count}'))
        self.stdout.write(self.style.SUCCESS(f'  - Remaining books: {Book.objects.count()}'))
        self.stdout.write('='*60)
