from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    """
    Django management command to seed the database with sample books.
    Usage: python manage.py seed_books
    """
    help = 'Seeds the database with sample book data for development'

    def handle(self, *args, **kwargs):
        """
        Main command logic to create sample books.
        """
        self.stdout.write(self.style.WARNING('Starting book seeding process...'))
        
        # Sample book data
        books_data = [
            {
                'title': 'Python Crash Course',
                'author': 'Eric Matthes',
                'isbn': '9781593279288',
                'category': 'Programming',
                'description': 'A hands-on, project-based introduction to programming with Python. '
                              'Perfect for beginners who want to learn Python quickly.',
                'quantity': 5,
                'available_quantity': 5
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'isbn': '9780132350884',
                'category': 'Programming',
                'description': 'A handbook of agile software craftsmanship. Learn how to write code '
                              'that is easy to read, maintain, and extend.',
                'quantity': 3,
                'available_quantity': 2
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt',
                'isbn': '9780135957059',
                'category': 'Programming',
                'description': 'Your journey to mastery. Timeless lessons for thinking about and '
                              'creating software that stands the test of time.',
                'quantity': 4,
                'available_quantity': 3
            },
            {
                'title': 'JavaScript: The Good Parts',
                'author': 'Douglas Crockford',
                'isbn': '9780596517748',
                'category': 'Programming',
                'description': 'A deep dive into the best features of JavaScript. Learn what makes '
                              'JavaScript an outstanding object-oriented programming language.',
                'quantity': 6,
                'available_quantity': 6
            },
            {
                'title': 'Design Patterns',
                'author': 'Erich Gamma',
                'isbn': '9780201633610',
                'category': 'Software Engineering',
                'description': 'Elements of Reusable Object-Oriented Software. Classic book covering '
                              '23 design patterns that solve common design problems.',
                'quantity': 3,
                'available_quantity': 1
            },
            {
                'title': 'Introduction to Algorithms',
                'author': 'Thomas H. Cormen',
                'isbn': '9780262033848',
                'category': 'Computer Science',
                'description': 'The definitive textbook on algorithms. Comprehensive coverage of a '
                              'broad range of algorithms in depth.',
                'quantity': 4,
                'available_quantity': 4
            },
            {
                'title': 'Eloquent JavaScript',
                'author': 'Marijn Haverbeke',
                'isbn': '9781593279509',
                'category': 'Programming',
                'description': 'A modern introduction to programming with JavaScript. Learn about '
                              'browser and server-side programming.',
                'quantity': 5,
                'available_quantity': 3
            },
            {
                'title': 'You Don\'t Know JS',
                'author': 'Kyle Simpson',
                'isbn': '9781491924464',
                'category': 'Programming',
                'description': 'Get started with JavaScript and web development. Deep dive into '
                              'the core mechanisms of the JavaScript language.',
                'quantity': 7,
                'available_quantity': 7
            },
            {
                'title': 'Head First Design Patterns',
                'author': 'Eric Freeman',
                'isbn': '9780596007126',
                'category': 'Software Engineering',
                'description': 'A brain-friendly guide to design patterns. Learn object-oriented design '
                              'principles and patterns in a fun and engaging way.',
                'quantity': 4,
                'available_quantity': 2
            },
            {
                'title': 'The Mythical Man-Month',
                'author': 'Frederick Brooks',
                'isbn': '9780201835953',
                'category': 'Software Engineering',
                'description': 'Essays on software engineering. Classic book about the challenges of '
                              'managing complex software projects.',
                'quantity': 2,
                'available_quantity': 2
            },
            {
                'title': 'Code Complete',
                'author': 'Steve McConnell',
                'isbn': '9780735619678',
                'category': 'Software Engineering',
                'description': 'A practical handbook of software construction. Covers all aspects of '
                              'software construction with best practices.',
                'quantity': 3,
                'available_quantity': 3
            },
            {
                'title': 'Refactoring',
                'author': 'Martin Fowler',
                'isbn': '9780134757599',
                'category': 'Programming',
                'description': 'Improving the design of existing code. Learn how to efficiently '
                              'refactor code to improve its structure without changing behavior.',
                'quantity': 4,
                'available_quantity': 1
            },
            {
                'title': 'Cracking the Coding Interview',
                'author': 'Gayle Laakmann McDowell',
                'isbn': '9780984782857',
                'category': 'Computer Science',
                'description': '189 programming questions and solutions. Essential preparation for '
                              'technical interviews at top tech companies.',
                'quantity': 8,
                'available_quantity': 5
            },
            {
                'title': 'Artificial Intelligence: A Modern Approach',
                'author': 'Stuart Russell',
                'isbn': '9780134610993',
                'category': 'Artificial Intelligence',
                'description': 'The leading textbook in artificial intelligence. Comprehensive coverage '
                              'of AI concepts, algorithms, and applications.',
                'quantity': 5,
                'available_quantity': 4
            },
            {
                'title': 'Deep Learning',
                'author': 'Ian Goodfellow',
                'isbn': '9780262035613',
                'category': 'Artificial Intelligence',
                'description': 'The definitive resource on deep learning. Written by pioneers in the '
                              'field, covers mathematical foundations and practical techniques.',
                'quantity': 6,
                'available_quantity': 6
            },
        ]
        
        created_count = 0
        skipped_count = 0
        
        for book_data in books_data:
            # Check if book already exists by ISBN (unique field)
            if Book.objects.filter(isbn=book_data['isbn']).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠ Book "{book_data["title"]}" already exists. Skipping...')
                )
                skipped_count += 1
                continue
            
            # Create the book
            book = Book.objects.create(**book_data)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created: "{book.title}" by {book.author}')
            )
            created_count += 1
        
        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ Seeding completed!'))
        self.stdout.write(self.style.SUCCESS(f'  - Books created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'  - Books skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'  - Total books in database: {Book.objects.count()}'))
        self.stdout.write('='*60)
