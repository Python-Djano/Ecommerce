from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
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


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profile_picture:  
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
        else:
            
            return format_html('<img src="{}" width="30" style="border-radius:50%;">', 'images/avatars.jpg')
            

    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')




admin.site.register(Account, AccountAdmin)  
admin.site.register(UserProfile, UserProfileAdmin)