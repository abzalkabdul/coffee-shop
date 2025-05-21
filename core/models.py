from email.mime import image
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.apps import apps
from  django.contrib.auth.models import User

class Drinks(models.Model):
    # category: Hot coffee, Cold coffee, Iced Energy
    SIZE_CHOICES = [('s', 'Short'), ('t', 'Tall'),
                    ('g', 'Grande'), ('v', 'Venti')]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    price = models.IntegerField()
    image = models.ImageField(upload_to='drinks/', blank=True, null=True)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Drinks"
        verbose_name_plural = "Drinks"
    
    def __str__(self):
        return self.name

    
class Food(models.Model):
    # category: Bakery, Lunch, Treats
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='food/', blank=True, null=True)
    quantity = models.IntegerField(default=1)

    class Meta: 
        verbose_name_plural = "Food"

    def __str__(self):
        return self.name


# Cart
class Cart(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) #Drinks or Food
    object_id = models.PositiveIntegerField() #just id
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_item_total_price(self):
        return self.content_object.price * self.quantity
    
    @classmethod
    def get_cart_total_price(cls):
        total = 0
        for item in cls.objects.all():
            total += item.content_object.price * item.quantity
        return total
    
    class Meta:
        verbose_name_plural = "Cart"

    def __str__(self):
        return f"{self.content_object}, {self.object_id}, {self.quantity}"
    
