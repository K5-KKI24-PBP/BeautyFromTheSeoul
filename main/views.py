from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from main.forms import AdForm
from main.models import AdEntry


def show_main(request):
    if request.user.is_staff:  # Admins can see all ads
        ads = AdEntry.objects.all()
    else:
        ads = AdEntry.objects.filter(is_approved=True)  # Non-admins see only approved ads
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

@staff_member_required
def approve_ad(request, id):
    ad = AdEntry.objects.get(pk=id)
    ad.is_approved = True
    ad.save()
    return redirect('main:show_main')
