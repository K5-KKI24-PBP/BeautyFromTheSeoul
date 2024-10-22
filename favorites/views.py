from django.shortcuts import render
from favorites.models import Favorite

# Create your views here.
def show_favorites(request):
    favorites = Favorite.objects.all()
    context = {
        'favorites': favorites
    }

    return render(request, 'favorites.html', context)

