from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from main.forms import AdForm
from main.models import AdEntry
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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

def get_ads_flutter(request):
    ads = AdEntry.objects.all()
    ads_data = [
        {
            "model": "main.adentry",
            "pk": str(ad.id),
            "fields": {
                "brand_name": ad.brand_name,
                "image": ad.image.url if hasattr(ad.image, 'url') else ad.image,
                "is_approved": ad.is_approved,
            },
        }
        for ad in ads
    ]
    return JsonResponse(ads_data, safe=False)

@csrf_exempt
def approve_ad_flutter(request, id):
    if request.method == "POST":
        ad = get_object_or_404(AdEntry, id=id)
        ad.is_approved = True
        ad.save()
        return JsonResponse({"status": True, "message": "Ad approved successfully"})
    return JsonResponse({"status": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_ad_flutter(request, id):
    if request.method == "DELETE":
        ad = get_object_or_404(AdEntry, id=id)
        ad.delete()
        return JsonResponse({"status": True, "message": "Ad deleted successfully"})
    return JsonResponse({"status": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def submit_ad_flutter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            brand_name = data.get("brand_name")
            image = data.get("image")  

            if not brand_name or not image:
                return JsonResponse({"status": False, "message": "Missing required fields"}, status=400)

            new_ad = AdEntry(brand_name=brand_name, image=image)
            new_ad.save()
            return JsonResponse({"status": True, "message": "Ad submitted successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"status": False, "message": "Invalid JSON data"}, status=400)
    return JsonResponse({"status": False, "message": "Invalid request method"}, status=405)
