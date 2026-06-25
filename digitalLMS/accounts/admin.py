from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


class ProfileInline(admin.StackedInline):
    """
    Inline admin for Profile model to display within User admin.
    """
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['role', 'phone', 'address', 'created_at']
    readonly_fields = ['created_at']


class UserAdmin(BaseUserAdmin):
    """
    Extended User admin with Profile inline.
    """
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff']
    
    def get_role(self, obj):
        """
        Display user role in list view.
        """
        return obj.profile.role if hasattr(obj, 'profile') else 'N/A'
    
    get_role.short_description = 'Role'


# Unregister the default User admin
admin.site.unregister(User)

# Register User with the extended UserAdmin
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    """
    list_display = [
        'user',
        'role',
        'phone',
        'created_at'
    ]
    
    list_filter = [
        'role',
        'created_at',
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'phone',
        'address'
    ]
    
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Role & Permissions', {
            'fields': ('role',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
    
    ordering = ['-created_at']
    
    list_per_page = 25
