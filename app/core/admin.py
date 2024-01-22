from django.contrib import admin

from core.models import Contact, SearchContacts


# admin.site.register(Contact)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'user')
    list_filter = ('full_name', 'phone_number', 'user')
    search_fields = ('full_name', 'phone_number', 'user')


@admin.register(SearchContacts)
class SearchContactsAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user')
    list_filter = ('phone_number', 'user')
    # search_fields = ('full_name', 'phone_number', 'user')