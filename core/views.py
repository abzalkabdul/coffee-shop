from unicodedata import category
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render
from .models import Drinks, Food, Cart
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.contenttypes.models import ContentType

from .forms import CreateUserForm

def user_registration(request): 
    form = CreateUserForm()

    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account for {user} was created! ')
             
            return redirect('login')

    return render(request, 'user_registration.html', context={'form': form})

def user_login(request):
    form = AuthenticationForm()

    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:menu-content')
        else:
            messages.error(request, "Invalid username or password")
        
    return render(request, 'user_login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return redirect('core:menu-content')


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
                                                           'specified_item': specified_item})

def cart(request):
    if request.method=="POST":
        action = request.POST.get("action")
        if action in ("decrease", "increase", "delete_item"):
            item_id = request.POST.get("item_id")
            get_item = Cart.objects.get(id=item_id)
            if action=="delete_item":
                get_item.delete()
            elif action=="decrease":
                get_item.quantity -= 1
                get_item.save()
            elif action=="increase":
                get_item.quantity += 1
                get_item.save()

        else:
            specified_item_id = request.POST.get("specified_item_id")
            specified_item_category = request.POST.get("specified_item_category")
            if specified_item_category in Drinks.objects.values_list('category', flat=True).distinct():
                content_type = ContentType.objects.get_for_model(Drinks)
                specified_item = Drinks.objects.get(pk=specified_item_id)
            else:
                content_type = ContentType.objects.get_for_model(Food)
                specified_item = Food.objects.get(pk=specified_item_id)

            cart_item, created_now = Cart.objects.get_or_create(
                    content_type=content_type,
                    object_id=specified_item_id,
                    defaults={'content_object': specified_item, 'quantity':1}
                )
            if not created_now:
                cart_item.quantity +=1
                cart_item.save()
    try:
        cart_items = Cart.objects.all()
    except cart_items.DoesNotExist: 
        return HttpResponse("Cart Items Not Found. \nPlease, Add Some Products")

    return render(request, 'cart.html', context={"cart_items": cart_items,
                                                 "total_price": Cart.get_cart_total_price})
