from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from favorites.models import Favorite, Products


def show_favorites(request):
    if not request.user.is_authenticated:
        return render(request, 'not_logged_in.html')  # Render a custom template

    favorites = Favorite.objects.filter(user=request.user).select_related('skincare_product').order_by('-created_at')
    return render(request, 'favorites.html', {'favorites': favorites})

def add_favorites(request, product_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    product = get_object_or_404(Products, product_id=product_id)

    favorite, created = Favorite.objects.get_or_create(user=request.user, skincare_product=product)

    if created:
        messages.success(request, f'{product.product_name} has been added to your favorites!')
    else:
        messages.info(request, f'{product.product_name} is already in your favorites.')

    return redirect('catalogue:show_products')

@login_required
def remove_favorites(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)
    favorite = Favorite.objects.filter(user=request.user, skincare_product=product)

    if favorite.exists():
        favorite.delete()
        messages.success(request, f'{product.product_name} has been removed from your favorites.')
    else:
        messages.error(request, f'{product.product_name} is not in your favorites.')

    return redirect('favorites:favorites')





