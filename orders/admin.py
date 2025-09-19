from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # How many blank order items to display
    readonly_fields = ('product', 'quantity')
    can_delete = True

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_date', 'total_items')
    list_filter = ('status', 'created_date')
    search_fields = ('customer__username', 'id')
    inlines = [OrderItemInline]
    ordering = ('-created_date',)

    # Custom method to show total items in an order
    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = 'Total Items'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__id', 'product__name')
