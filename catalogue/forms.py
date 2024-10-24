from django import forms
from catalogue.models import Products
from django.forms import ModelForm

class ProductFilterForm(forms.Form):
    product_brand = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Brand'}))
    product_type = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Product Type'}))


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'product_brand', 'product_type', 'product_description', 'price']
