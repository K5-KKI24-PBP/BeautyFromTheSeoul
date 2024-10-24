from django.db import models
import uuid

class AdEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    brand_name = models.CharField(max_length=100)
    image = models.URLField(max_length=300)
    is_approved = models.BooleanField(default=False)
