from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {
            "fields": ("user_type", "bio", "profile_image", "has_access")
        }),
    )
    list_display = ("username", "email", "user_type", "is_staff", "is_superuser")
    list_filter = ("user_type", "is_staff", "is_superuser")
    search_fields = ("username", "email")
