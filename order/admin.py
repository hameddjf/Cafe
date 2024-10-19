from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Order, OrderItem


# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_menu_items',
                    'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'order_items__menu_item__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('total_price', 'created_at')
    inlines = [OrderItemInline]

    fieldsets = (
        (_('اطلاعات سفارش'), {
            'fields': ('user',)
        }),
        (_('جزئیات'), {
            'fields': ('total_price', 'created_at')
        }),
    )

    def get_menu_items(self, obj):
        return ", ".join([f"{item.menu_item.name} ({item.get_size_display()})" for item in obj.order_items.all()])
    get_menu_items.short_description = _('آیتم‌های منو')

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = _('قیمت کل')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'size', 'quantity', 'total_price')
    list_filter = ('size',)
    search_fields = ('order__user__username', 'menu_item__name')
