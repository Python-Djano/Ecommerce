from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name')
    search_fields = ('first_name', 'username')
    filter_horizontal = ()
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)