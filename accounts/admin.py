from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username", "email", "first_name", "last_name",
        "is_staff", "bio", "profile_picture_preview"
    )
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("bio", "profile_picture", "profile_picture_preview")
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("bio", "profile_picture")}),
    )

    readonly_fields = ("profile_picture_preview",)

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="120" height="120" '
                'style="object-fit: cover; border-radius: 50%; box-shadow: 0 2px 6px rgba(0,0,0,0.2);" />',
                obj.profile_picture
            )
        return "No Image"
    profile_picture_preview.short_description = "Profile Picture Preview"
