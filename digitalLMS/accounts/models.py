from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    User profile model extending Django's User model.
    """
    ROLE_CHOICES = [
        ('Member', 'Member'),
        ('Librarian', 'Librarian'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="Associated user account"
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Member',
        help_text="User role in the system"
    )
    
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Contact phone number"
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Full address"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Profile creation date and time"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        """
        String representation of the Profile model.
        """
        return f"{self.user.username} - {self.role}"
    
    def is_librarian(self):
        """
        Check if the user is a librarian.
        """
        return self.role == 'Librarian'
    
    def is_member(self):
        """
        Check if the user is a member.
        """
        return self.role == 'Member'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a Profile when a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to automatically save the Profile when a User is saved.
    """
    # Check if profile exists, if not create it
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
