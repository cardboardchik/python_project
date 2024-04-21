from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=500)
    img_links = models.CharField(max_length=500)


class Item(models.Model):
    name = models.CharField(max_length=128)
    characteristics = models.JSONField(encoder=None)
    description = models.TextField(max_length=500)
    img_links = models.JSONField(encoder=None)
    price = models.IntegerField(default=10)
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)


class Reviews(models.Model):
    rating = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.CharField(max_length=256, null=True)
    date = models.DateField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)