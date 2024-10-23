from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
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

def delete_ad(request, id):
    ad = AdEntry.objects.get(pk = id)
    ad.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def edit_ad(request, id):
    ad = AdEntry.objects.get(pk = id)

    form = AdForm(request.POST or None, instance=ad)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_ad.html", context)