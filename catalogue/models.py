from django.db import models
import uuid

# Create your models here.
class Products(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=100)
    product_brand = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    product_description = models.TextField()
    price = models.CharField(max_length=100)
    image = models.URLField()

