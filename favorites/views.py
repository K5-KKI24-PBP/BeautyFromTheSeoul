from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from favorites.models import Favorite, Products
from catalogue.models import Review
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json


def show_favorites(request):
    if not request.user.is_authenticated:
        return render(request, 'not_logged_in.html')  # Render a custom template

    favorites = Favorite.objects.filter(user=request.user).select_related('skincare_product')

    # Collect unique product types from the favorites list
    product_types = favorites.values_list('skincare_product__product_type', flat=True).distinct()
    product_types = sorted(set(product_types))  # Sort and remove duplicates

    # Get sorting option
    sort_option = request.GET.get('sort', 'recent')
    if sort_option == 'most_oldest':
        favorites = favorites.order_by('created_at')  # Oldest first
    else:
        favorites = favorites.order_by('-created_at')  # Most recent first

    # Filtering logic for skincare type
    product_type = request.GET.get('product_type')
    if product_type:
        favorites = favorites.filter(skincare_product__product_type__icontains=product_type)

    # Check if the user has reviewed each product
    for favorite in favorites:
        favorite.skincare_product.user_reviewed = Review.objects.filter(
            product=favorite.skincare_product,
            user=request.user
        ).exists()

    context = {
        'favorites': favorites,
        'product_types': product_types,
        'selected_product_type': product_type  # To retain the selected filter
    }

    return render(request, 'favorites.html', context)

def add_favorites(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You need to log in to add to favorites.'}, status=403)
    
    product = get_object_or_404(Products, product_id=product_id)

    favorite, created = Favorite.objects.get_or_create(user=request.user, skincare_product=product)

    if created:
        # Added to favorites
        return JsonResponse({'added': True})
    else:
        # Already a favorite, so remove it
        favorite.delete()
        return JsonResponse({'removed': True})

def remove_favorites(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'You need to be logged in to remove favorites.'}, status=401)
    
    product = get_object_or_404(Products, product_id=product_id)
    favorite = Favorite.objects.filter(user=request.user, skincare_product=product)

    if favorite.exists():
        favorite.delete()
        return JsonResponse({'success': True, 'message': 'Your favorite product has been removed from your favorites.'})
    else:
        return JsonResponse({'success': False, 'message': 'The following product is not in your favorites.'})

@csrf_exempt
def get_favorites(request):
    if request.method == 'POST':
        # Parse the request body
        data = json.loads(request.body)
        user_id = data.get('user_id')  # Get the user_id from the request body

        if not user_id:
            return JsonResponse({'error': 'User ID is missing'}, status=400)

        # Fetch the user's favorites
        favorites = Favorite.objects.filter(user_id=user_id).select_related('skincare_product')
        print(favorites)

        # Serialize the favorite products
        favorite_products = [
            {
                'name': favorite.skincare_product.product_name,
                'brand': favorite.skincare_product.product_brand,
                'price': favorite.skincare_product.price,
                'image': favorite.skincare_product.image,
            }
            for favorite in favorites
        ]

        # Return the favorites as a JSON response
        return JsonResponse(favorite_products, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def add_favorites_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        product_id = data.get('product_id') 
        if not product_id:
            return JsonResponse({'error': 'Product ID is missing'}, status=400)

        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'user ID is missing'}, status=400)

        # Fetch the product instance based on the product_id
        try:
            product = Products.objects.get(product_id=product_id)  # Adjust if using a different identifier
        except Products.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        # Fetch or create the favorite for the user
        favorite, created = Favorite.objects.get_or_create(user_id=user_id, skincare_product=product)
        if not created:
            favorite.delete()  # If it exists, remove it
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})

    return JsonResponse({'error': 'Invalid request'}, status=400)