from django.contrib import admin

from .models import Order, OrderItem, Address


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    verbose_name = "Пункт заказа"
    verbose_name_plural = "Пункты заказа"

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('client__username', 'client__first_name', 'client__last_name')
    list_display = ('client', 'status', 'address', 'created_at')
    list_filter = ('status',)
    change_list_template = "orders_admin.html"
    inlines = [OrderItemInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'house_number', 'apartment_number')
