from django.contrib import admin

from core.models import CustomUser
from core.models import Contact

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'phone_number')

@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    list_filter = ('first_name', 'last_name', 'phone_number')
    search_fields = ('first_name', 'last_name', 'phone_number')