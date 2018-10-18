from django.contrib import admin

from .models import Order, OrderItem, Address


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    verbose_name = "Пункт заказа"
    verbose_name_plural = "Пункты заказа"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'status', 'address', 'created_at')
    list_filter = ('status', )

    inlines = [OrderItemInline]

    def get_readonly_fields(self, request, obj=None):
        return 'address', 'status'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'house_number', 'apartment_number')
