from django.shortcuts import render, redirect
from main.forms import AdForm
from main.models import AdEntry

def show_main(request):
    ads = AdEntry.objects.all()
    context = {
        "user": request.user,
        "ads": ads
        }
    return render(request, "main.html", context)

def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:show_main')  
    else:
        form = AdForm()
    return render(request, 'create_ads.html', {'form': form})
