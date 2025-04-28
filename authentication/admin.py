# authentication/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PasswordResetRequest

class CustomUserAdmin(admin.ModelAdmin):
    # Update 'list_display' to use 'email' instead of 'username'
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined')

    # You can also add 'search_fields' or other configurations as needed
    search_fields = ('email', 'first_name', 'last_name')

    # You can add fieldsets or other customizations to the admin interface as needed
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'role')}),
    )

    # Add form configuration for password, etc.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    readonly_fields = ('user', 'token', 'created_at')
    search_fields = ('user__email',)
