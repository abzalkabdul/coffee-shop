from django.contrib import admin

from .models import Drinks, Food, Cart, Ticket

@admin.register(Drinks)
class DrinksAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'category', 'price', 'quantity', 'size']
    search_display=['name', 'category']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'quantity']
    search_display = ['name', 'category']

admin.site.register(Cart)
admin.site.register(Ticket)