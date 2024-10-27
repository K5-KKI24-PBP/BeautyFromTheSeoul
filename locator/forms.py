from django import forms
from django.forms import ModelForm
from locator.models import Locations
from django.utils.html import strip_tags

class StoreLocationForm(ModelForm):
    class Meta:
        model = Locations
        fields = ["store_name", "street_name", "district", "gmaps_link", "store_image"]
        widgets = {
            'store_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Store Name'
            }),
            'street_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Street Name'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter District'
            }),
            'gmaps_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Google Maps Link'
            }),
            'store_image': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Link Image'
            }),
        }

    def clean_store_name(self):
        store_name = self.cleaned_data.get("store_name")
        return strip_tags(store_name)

    def clean_street_name(self):
        street_name = self.cleaned_data.get("street_name")
        return strip_tags(street_name)

    def clean_district(self):
        district = self.cleaned_data.get("district")
        return strip_tags(district)

    def clean_gmaps_link(self):
        gmaps_link = self.cleaned_data.get("gmaps_link")
        if gmaps_link:
            if not gmaps_link.startswith("https://"):
                raise forms.ValidationError("Google Maps link must start with 'https://'")
        else:
            raise forms.ValidationError("This field is required.")
        return gmaps_link

    def clean_store_image(self):
        store_image = self.cleaned_data.get("store_image")
        return strip_tags(store_image)