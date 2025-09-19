from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active', 'created_at', 'low_stock_alert')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    # Custom method to show low stock
    def low_stock_alert(self, obj):
        if obj.stock_quantity <= 5:  # threshold
            return "⚠️ Low Stock"
        return ""
    low_stock_alert.short_description = 'Stock Alert'
