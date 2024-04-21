from django.db import models

from django.db import models
from store.models import Item
from users.models import User
from django.core.validators import MinValueValidator 

class Cart(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.item.price * self.quantity
    def __unicode__(self):
        return self.item