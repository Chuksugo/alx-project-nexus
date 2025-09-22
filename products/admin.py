from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock_quantity", "image_tag")
    list_filter = ("category",)
    search_fields = ("name", "description", "category__name")
    list_editable = ("price", "stock_quantity")

    def image_tag(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;"/>',
                obj.image_url,
            )
        return "No Image"

    image_tag.short_description = "Image"
