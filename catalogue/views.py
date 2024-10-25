from django.shortcuts import render, redirect
from catalogue.forms import AddProductForm, ProductFilterForm
from catalogue.models import Products
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse
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
    
    product_type = request.GET.get('product_type')
    product_brand = request.GET.get('brand')
    image = request.GET.get('image')

    print(f"Product Name: {product_type}, Product Brand: {product_brand}, Image: {image}")

    if product_type or product_brand or image:
        if product_type:  
            products = products.filter(product_type__icontains=product_type)
        if product_brand:
            products = products.filter(product_brand__icontains=product_brand)
        if image:
            products = products.filter(image__icontains=image)

    context = {
        'products': products,
        'form': form
    }
    return render(request, "catalogue.html", context)

# Editing product
@superuser_required
@login_required
def edit_product(request):
    product = Products.objects.get()

    form = AddProductForm(request.POST or None, instance=product)

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
    image= strip_tags(request.POST.get("image"))
    product_name = strip_tags(request.POST.get("name"))
    product_brand = strip_tags(request.POST.get("brand"))
    product_type  = strip_tags(request.POST.get("product_type"))
    product_description = strip_tags(request.POST.get("description"))
    price = strip_tags(request.POST.get("price"))
    user = request.user

    if not all([image, product_name, product_brand, product_type, product_description, price]):
        return JsonResponse({"error": "Fill in all required fields!"}, status=400)
    
    try:
        new_product = Products(
            name=product_name, brand=product_brand,
            product_type=product_type, description=product_description,
            price=price, image=image,
            user=user
        )
        new_product.save()
        return HttpResponse(b"Product Added Successfully.", status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def get_product(request):
    data = Products.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')
    
