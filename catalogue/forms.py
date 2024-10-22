from django import forms
from catalogue.models import Products

class ProductFilterForm(forms.Form):
    brand = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Brand'}))
    product_type = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Product Type'}))


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'brand', 'product_type', 'description', 'price']
