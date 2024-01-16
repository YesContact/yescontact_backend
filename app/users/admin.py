from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm
)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ('email', 'full_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        ('User Information', {'fields': ('full_name', 'phone_number', 'email', 'password', 'profile_photo', 'wallet')}),
        # ('Permissions', {'fields': ('is_staff', 'is_active',
        #  'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'full_name', 'phone_number', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
         ),
    )
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('full_name',)


admin.site.register(CustomUser, CustomUserAdmin)
