from django.shortcuts import render, redirect
from catalogue.forms import AddProductForm, ProductFilterForm, ReviewForm
from catalogue.models import Products, Review
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
        'form': form,
        'product_form': AddProductForm()
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
@require_POST
def delete_product(request, product_id):
    try:
        product = Products.objects.get(pk=product_id)
        product.delete()
        return redirect(reverse('catalogue:show_products'))
    except Products.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_POST
def add_product_entry(request):
    image= strip_tags(request.POST.get("image"))
    product_name = strip_tags(request.POST.get("product_name"))
    product_brand = strip_tags(request.POST.get("product_brand"))
    product_type  = strip_tags(request.POST.get("product_type"))
    product_description = strip_tags(request.POST.get("product_description"))
    price = strip_tags(request.POST.get("price"))
    

    if not all([image, product_name, product_brand, product_type, product_description, price]):
        return JsonResponse({"error": "Fill in all required fields!"}, status=400)
    
    try:
        new_product = Products(
            product_name=product_name, product_brand=product_brand,
            product_type=product_type, product_description=product_description,
            price=price, image=image,
        )
        new_product.save()
        return redirect(reverse('catalogue:show_products'))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def get_product(request):
    data = Products.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')
    
@login_required
@require_POST
def add_review(request, product_id):
    product = Products.objects.get(pk=product_id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review, created = Review.objects.get_or_create(
            product=product,
            user=request.user,
            defaults={'rating': form.cleaned_data['rating'], 'comment': form.cleaned_data['comment']}
        )
        if not created:  # If review exists, update it
            review.rating = form.cleaned_data['rating']
            review.comment = form.cleaned_data['comment']
            review.save()
        return redirect(reverse('catalogue:show_products'))
    else:
        return JsonResponse({"error": "Invalid data provided."}, status=400)
    
@superuser_required
@login_required
@require_POST
def delete_review(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
        review.delete()
        return redirect(reverse('catalogue:show_products'))
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)