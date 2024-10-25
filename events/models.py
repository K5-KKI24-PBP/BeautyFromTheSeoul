from django.db import models
import uuid
from authentication.models import UserProfile
from django.core.exceptions import ValidationError

class Events(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField() #format: YYYY-MM-DD
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    promotion_type = models.CharField(max_length=200)

class RSVP(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rsvp_status = models.BooleanField(default=False)
