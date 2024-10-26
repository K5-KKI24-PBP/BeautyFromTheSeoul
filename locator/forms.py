from django import forms
from django.forms import ModelForm
from locator.models import Locations

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

    def clean_gmaps_link(self):
        gmaps_link = self.cleaned_data.get("gmaps_link")
        if gmaps_link:
            if not gmaps_link.startswith("https://"):
                raise forms.ValidationError("Google Maps link must start with 'https://'")
        else:
            raise forms.ValidationError("This field is required.")  # Validasi untuk field yang kosong
        return gmaps_link

