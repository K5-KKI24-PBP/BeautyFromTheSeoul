from django.shortcuts import render, redirect
from catalogue.forms import AddProductForm, ProductFilterForm
from catalogue.models import Products
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.urls import reverse
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

# Create your views here.
def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied. You must be a superuser to access this page.")
    return _wrapped_view

def show_products(request):
    products = Products.objects.all()
    form = ProductFilterForm(request.GET)
    
    if form.is_valid():
        product_name = form.cleaned_data.get('name')
        product_brand = form.cleaned_data.get('brand')  
        
        if product_name:
            products = products.filter(name__icontains=product_name)
        if product_brand:
            products = products.filter(brand__icontains=product_brand)

    context = {
        'products': products,
        'form': form
    }
    return render(request, "catalogue.html", context)

# Add Product
@superuser_required
@login_required
def add_product(request):
    form = AddProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)


# Editing product
@superuser_required
@login_required
def edit_product(request):
    product = Products.objects.get()

    form = Products(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

# Delete Product
@superuser_required
@login_required
def delete_product():
    product = Products.objects.get()
    
    product.delete()

    return HttpResponseRedirect(reverse('main:show_main'))
@csrf_exempt
@require_POST
def add_product_entry(request):
    product_name = strip_tags(request.POST.get("name"))
    product_brand = strip_tags(request.POST.get("brand"))
    product_type  = strip_tags(request.POST.get("product_type"))
    product_description = strip_tags(request.POST.get("description"))
    price = strip_tags(request.POST.get("price"))
    user = request.user

    new_product = Products(
        name=product_name, brand=product_brand,
        product_type=product_type, description=product_description,
        price=price,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

def get_product(request):
    data = Products.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')
    
