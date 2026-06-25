from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    """
    Django management command to create profiles for existing users.
    Usage: python manage.py create_profiles
    """
    help = 'Creates profiles for existing users who do not have one'

    def handle(self, *args, **kwargs):
        """
        Main command logic to create missing profiles.
        """
        self.stdout.write(self.style.WARNING('Creating profiles for existing users...'))
        
        created_count = 0
        skipped_count = 0
        
        # Get all users
        users = User.objects.all()
        
        for user in users:
            # Check if user already has a profile
            if hasattr(user, 'profile'):
                self.stdout.write(
                    self.style.WARNING(f'⚠ User "{user.username}" already has a profile. Skipping...')
                )
                skipped_count += 1
            else:
                # Create profile for user
                Profile.objects.create(user=user)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created profile for user: "{user.username}"')
                )
                created_count += 1
        
        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ Profile creation completed!'))
        self.stdout.write(self.style.SUCCESS(f'  - Profiles created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'  - Users skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'  - Total users: {users.count()}'))
        self.stdout.write('='*60)
