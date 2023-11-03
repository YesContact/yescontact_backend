from django.contrib import admin

from core.models import Contact


@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number")
    list_filter = ("first_name", "last_name", "phone_number")
    search_fields = ("first_name", "last_name", "phone_number")
