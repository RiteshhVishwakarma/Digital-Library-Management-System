"""
Management command to seed default book categories.
"""
from django.core.management.base import BaseCommand
from books.models import Category


class Command(BaseCommand):
    help = 'Seed default book categories'

    def handle(self, *args, **kwargs):
        """
        Create default categories if they don't exist.
        """
        categories = [
            {
                'name': 'Programming',
                'description': 'Books about programming languages, software development, algorithms, and computer science.'
            },
            {
                'name': 'Fiction',
                'description': 'Novels, short stories, and other works of imaginative literature.'
            },
            {
                'name': 'Science',
                'description': 'Books about natural sciences, physics, chemistry, biology, and scientific research.'
            },
            {
                'name': 'History',
                'description': 'Books about historical events, civilizations, and important periods in human history.'
            },
            {
                'name': 'Biography',
                'description': 'Life stories and autobiographies of notable individuals from various fields.'
            },
            {
                'name': 'Technology',
                'description': 'Books about modern technology, innovation, digital transformation, and tech trends.'
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        self.stdout.write(self.style.MIGRATE_HEADING('Seeding categories...'))
        
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created category: {category.name}')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'- Category already exists: {category.name}')
                )
        
        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f'\nSummary: {created_count} created, {existing_count} already existed'
            )
        )
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully seeded {created_count} new categories!')
            )
