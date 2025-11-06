from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'firstname', 'lastname',
                    'role', 'is_staff', 'date_created']
    list_filter = ['role', 'is_staff', 'date_created']
    search_fields = ['email', 'firstname', 'lastname']
    ordering = ['-date_created']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('firstname', 'lastname', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_created')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'firstname', 'lastname', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['date_created', 'last_login']
