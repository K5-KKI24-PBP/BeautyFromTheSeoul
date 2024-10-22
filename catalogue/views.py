from django.shortcuts import render, redirect
from catalogue.forms import AddProductForm
from catalogue.models import Products

# Create your views here.
def show_products(request):
    products = Products.objects.all()

    context = {
        'products': products
    }

    return render(request, 'catalogue.html', context)