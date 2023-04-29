from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_slug')
    prepopulated_fields = {'category_slug': ('category_name',)}


admin.site.register(Category, CategoryAdmin)