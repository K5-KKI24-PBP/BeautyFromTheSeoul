from django.db import models

# Create your models here.
class Locations(models.Model):
    store_name = models.CharField(max_length = 100)
    store_address = models.CharField(max_length = 300)
    website = models.URLField(max_length=200, blank=True, null=True)


