from django.db import models
import uuid

class Locations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    store_name = models.CharField(max_length = 100)
    street_name = models.CharField(max_length = 300)
    district = models.CharField(max_length = 100)
    gmaps_link = models.URLField(max_length=500, blank=True, null=True)
    store_image = models.URLField(max_length=300)