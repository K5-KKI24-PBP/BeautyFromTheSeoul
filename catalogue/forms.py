from django import forms
from catalogue.models import Products, Review
from django.forms import ModelForm

class ProductFilterForm(forms.Form):
    product_brand = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Brand'}))
    product_type = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Product Type'}))
    image = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Image'}))


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'product_brand', 'product_type', 'product_description', 'price', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
            'comment': forms.Textarea(attrs={'placeholder': 'Write your review here...'}),
        }