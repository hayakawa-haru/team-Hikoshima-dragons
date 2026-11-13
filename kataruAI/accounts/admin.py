from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "create_at", "update_at", "deleted_at", "is_active")
    search_fields = ("username", "email")
