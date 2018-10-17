from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    verbose_name = "Пункт заказа"
    verbose_name_plural = "Пункты заказа"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'confirmed', 'canceled', 'created_at')
    list_filter = ('confirmed', 'canceled')

    inlines = [OrderItemInline]
