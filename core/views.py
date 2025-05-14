from os import name
from sys import intern
from django.views import generic
from django.shortcuts import render
from .models import Drinks, Food
from django.shortcuts import render

class MenuView(generic.ListView):
    context_object_name = 'menu_items'
    template_name = 'menu-content.html'
    
    def get_queryset(self):
        return list(Drinks.objects.all()) + list(Food.objects.all())
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['food_items'] = Food.objects.all()
        context['drinks_items'] = Drinks.objects.all()
        
        # Two context names for drinks
        context['drinks_categories'] = Drinks.objects.values_list('category', flat=True).distinct()
        drinks_categories_with_image = {}
        for category in context['drinks_categories']:
            item = Drinks.objects.filter(category=category, image__isnull=False).first()
            drinks_categories_with_image[f'{category}'] = item.image.url
        context['drinks_categories_with_image'] = drinks_categories_with_image

        # Two context names for food
        context['food_categories'] = Food.objects.values_list('category', flat=True).distinct()
        food_categories_with_image = {}
        for category in context['food_categories']:
            item = Food.objects.filter(category=category, image__isnull=False).first()
            food_categories_with_image[f'{category}'] = item.image.url
        context['food_categories_with_image'] = food_categories_with_image

        return context
    

def menu_specified(request, category):
    category_items = Drinks.objects.filter(category=category)
    if not category_items.exists():
        category_items = Food.objects.filter(category=category)

    drinks_categories = Drinks.objects.values_list('category', flat=True).distinct()
    food_categories = Food.objects.values_list('category', flat=True).distinct()
    return render(request, 'menu-content-specified.html', {'category_items': category_items,
                                                           'category': category,
                                                           'drinks_categories': drinks_categories,
                                                           'food_categories': food_categories})


def specified_item(request, category, item_id):
    drinks_categories = Drinks.objects.values_list('category', flat=True).distinct()
    food_categories = Food.objects.values_list('category', flat=True).distinct()

    specified_item_name = Drinks.objects.get(pk=item_id).name
    specified_item = Drinks.objects.get(pk=item_id)
    if not specified_item_name or not Drinks.objects.filter(category=category):
        specified_item_name = Food.objects.get(pk=item_id).name
        specified_item = Food.objects.get(pk=item_id)
        

    return render(request, 'specified-item.html', context={'category': category,
                                                          'item_id': item_id,
                                                          'food_categories': food_categories,
                                                          'drinks_categories': drinks_categories,
                                                          'specified_item_name': specified_item_name,
                                                           'specified_item': specified_item })
                                                          

def rewards_view(request):
    return render(request, 'rewards.html')


def gift_cards_view(request):
    return render(request, 'gift_cards.html')
