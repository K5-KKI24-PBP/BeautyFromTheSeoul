from django import forms
from django.forms import ModelForm
from main.models import AdEntry
from django.utils.html import strip_tags

class AdForm(ModelForm):
    class Meta:
        model = AdEntry
        fields = ["brand_name", "image"]

        widgets = {
            'brand_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Brand Name',
            }),
            'image': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Image URL',
            }),
        }

    def clean_brand_name(self):
        brand_name = self.cleaned_data.get("brand_name")
        return strip_tags(brand_name)

    def clean_image(self):
        image = self.cleaned_data.get("image")
        return strip_tags(image)