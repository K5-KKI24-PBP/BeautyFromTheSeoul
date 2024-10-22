from django.forms import ModelForm
from main.models import AdEntry

class AdForm(ModelForm):
    class Meta:
        model = AdEntry
        fields = ["brand_name", "image"]