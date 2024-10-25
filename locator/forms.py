from django.forms import ModelForm
from locator.models import Locations

class StoreLocationForm(ModelForm):
    class Meta:
        model = Locations
        fields = ["store_name", "street_name", "district", "gmaps_link", "store_image"]