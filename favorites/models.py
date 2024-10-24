from django.db import models
from django.contrib.auth.models import User
from catalogue.models import Products

# Create your models here.
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skincare_product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'skincare_product')