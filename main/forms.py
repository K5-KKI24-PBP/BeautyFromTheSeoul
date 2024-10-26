from django import forms
from django.forms import ModelForm
from main.models import AdEntry

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
