from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.user_role}"