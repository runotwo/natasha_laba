from django.contrib import admin

from .models import Good, Category


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'count')
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
