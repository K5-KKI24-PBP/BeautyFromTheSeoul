from django import forms
from catalogue.models import Products, Review
from django.forms import ModelForm
from django.utils.html import strip_tags

class ProductFilterForm(forms.Form):
    product_brand = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Brand'}))
    product_type = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Product Type'}))
    image = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Image'}))


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'product_brand', 'product_type', 'product_description', 'price', 'image']
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter name of product'
            }),
            'product_brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter brand of product'
            }),
            'product_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter type of product'
            }),
            'product_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'image': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image URL'
            }),
        }

    def clean_image(self):
        image = self.cleaned_data["image"]
        return strip_tags(image)
    
    def clean_product_name(self):
        product_name = self.cleaned_data["product_name"]
        return strip_tags(product_name)
    
    def clean_product_brand(self):
        product_brand = self.cleaned_data["product_brand"]
        return strip_tags(product_brand)
    
    def clean_product_type(self):
        product_type = self.cleaned_data["product_type"]
        return strip_tags(product_type)
    
    def clean_product_description(self):
        product_description = self.cleaned_data["product_description"]
        return strip_tags(product_description)
    
    def clean_price(self):
        price = self.cleaned_data["price"]
        return strip_tags(price)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
            'comment': forms.Textarea(attrs={'placeholder': 'Write your review here...'}),
        }
        
    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        return strip_tags(rating)
    
    def clean_comment(self):
        comment = self.cleaned_data["comment"]
        return strip_tags(comment)