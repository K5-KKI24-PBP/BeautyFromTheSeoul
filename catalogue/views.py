from django.shortcuts import render, redirect, get_object_or_404
from catalogue.forms import AddProductForm, ProductFilterForm, ReviewForm
from catalogue.models import Products, Review
from favorites.models import Favorite
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse
from django.urls import reverse
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib import messages
from django.template.loader import render_to_string
import json
from datetime import datetime
from authentication.models import User

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
    product_types = Products.objects.values_list('product_type', flat=True).distinct()
    product_brands = Products.objects.values_list('product_brand', flat=True).distinct()
    
    favorite_product_ids = (
        list(Favorite.objects.filter(user=request.user).values_list('skincare_product__product_id', flat=True))
        if request.user.is_authenticated else []
    )

    form = ProductFilterForm(request.GET)
    products = filter_products(request, products)

    user_reviews = {}
    if request.user.is_authenticated:
        user_reviews = {
            review.product_id: review
            for review in Review.objects.filter(
                user=request.user,
                product_id__in=[product.product_id for product in products]
            )
        }

    for product in products:
        product.user_reviewed = product.product_id in user_reviews

    context = {
        'products': products,
        'form': form,
        'product_form': AddProductForm(),
        'user_reviews': user_reviews,
        'product_types': product_types,
        'product_brands': product_brands,
        'favorite_product_ids': favorite_product_ids,
    }
    
    return render(request, "catalogue.html", context)

def filter_products(request, products):
    product_type = request.GET.get('product_type')
    product_brand = request.GET.get('product_brand')
    
    print(product_type)
    print(product_brand)

    if product_type:
        products = products.filter(product_type__icontains=product_type)
    if product_brand:
        products = products.filter(product_brand__icontains=product_brand)

    return products

def filter_products_ajax(request):
    products = Products.objects.all()  # Get all products initially
    products = filter_products(request, products)  # Apply the filtering criteria

    # Render the filtered products list to HTML
    html = render_to_string('product_list.html', {'products': products}, request=request)
    return JsonResponse({'html': html})

# Editing product
@superuser_required
@login_required
def edit_product(request, product_id):
    print(f"Received product_id: {product_id}") 

    product = get_object_or_404(Products, pk=product_id)
    print(f"Product found: {product.product_name}") 
    
    form = AddProductForm(request.POST or None, instance=product)

    if request.method == "POST":
        print("Request data:", request.POST) 

        # Validate the form
        if form.is_valid():
            form.save()
            return redirect(reverse('catalogue:show_products'))
        else:
            return JsonResponse({"success": False, "errors": form.errors})

    form_html = form.as_p()
    return JsonResponse({
        "form_html": form_html,
        "product_data": {
            "product_name": product.product_name,
            "product_brand": product.product_brand,
            "product_type": product.product_type,
            "product_description": product.product_description,
            "price": product.price,
            "image": product.image,
        }
    })

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
@superuser_required
def add_product_entry(request):
    image = strip_tags(request.POST.get("image"))
    product_name = strip_tags(request.POST.get("product_name"))
    product_brand = strip_tags(request.POST.get("product_brand"))
    product_type = strip_tags(request.POST.get("product_type"))
    product_description = strip_tags(request.POST.get("product_description"))
    price = strip_tags(request.POST.get("price"))
    
    if not all([image, product_name, product_brand, product_type, product_description, price]):
        return JsonResponse({"error": "Fill in all required fields!"}, status=400)
    
    try:
        new_product = Products(
            product_name=product_name,
            product_brand=product_brand,
            product_type=product_type,
            product_description=product_description,
            price=price,
            image=image,
        )
        new_product.save()

        # After saving, render the updated product list
        products = Products.objects.all()  # Get updated product list
        html = render_to_string('product_list.html', {'products': products}, request=request)
        
        return JsonResponse({'html': html})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
def get_product(request):
    data = Products.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')
    
@csrf_exempt
@login_required
@require_POST
def add_review(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    form = ReviewForm(request.POST)
    user_review = Review.objects.filter(user=request.user, product=product).first()

    if user_review:
        return JsonResponse({"error": "You have already reviewed this product."}, status=400)

    if form.is_valid():
        review, created = Review.objects.get_or_create(
            product=product,
            user=request.user,
            defaults={'rating': form.cleaned_data['rating'], 'comment': form.cleaned_data['comment']}
        )
        if not created:  
            review.rating = form.cleaned_data['rating']
            review.comment = form.cleaned_data['comment']
            review.save()
        return redirect(reverse('catalogue:show_products'))
    else:
        messages.error(request, "Invalid data provided/Review from User already exists .")
        return redirect(reverse('catalogue:show_products'))
    
@csrf_exempt
@superuser_required
@login_required
@require_POST
def delete_review(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
        review.delete()
        return JsonResponse({"success": True, "message": "Review deleted successfully."})
    except Review.DoesNotExist:
        return JsonResponse({"success": False, "message": "Review not found."}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

def get_review(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

@csrf_exempt
def review_flutter(request, product_id):
    if request.method == 'POST':
        try:
            # Add debug logging
            print(f"Processing review for product {product_id}")
            
            data = json.loads(request.body)
            
            # Validate data first
            user_id = data.get('user')
            rating = data.get('rating')
            comment = data.get('comment')
            
            # Check for existing review first
            try:
                user = User.objects.get(pk=user_id)
                product = Products.objects.get(pk=product_id)
                
                existing_review = Review.objects.filter(
                    product=product, 
                    user=user
                ).exists()
                
                if existing_review:
                    return JsonResponse({
                        "status": False,
                        "message": "You have already reviewed this product"
                    }, status=400)
                    
                # Create review only if no existing review
                review = Review.objects.create(
                    product=product,
                    user=user, 
                    rating=rating,
                    comment=comment
                )
                
                return JsonResponse({
                    "status": True,
                    "message": "Review created successfully"
                }, status=201)
                
            except (User.DoesNotExist, Products.DoesNotExist) as e:
                return JsonResponse({
                    "status": False, 
                    "message": str(e)
                }, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON"
            }, status=400)
            
        except Exception as e:
            print(f"Error creating review: {str(e)}")
            return JsonResponse({
                "status": False,
                "message": str(e) 
            }, status=500)

    return JsonResponse({
        "status": False,
        "message": "Invalid method"
    }, status=405)