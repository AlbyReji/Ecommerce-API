from django.db import models
from django.contrib.auth.models import AbstractUser
from admin_api.models import (Category,
                              Product)

class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"