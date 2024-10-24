from django.forms import ModelForm
from locator.models import Locations

class StoreLocationForm(ModelForm):
    class Meta:
        model = Locations
        fields = ["store_name", "store_address", "website"]