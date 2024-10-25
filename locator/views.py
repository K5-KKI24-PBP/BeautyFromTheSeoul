from django.shortcuts import render, redirect, reverse
from locator.forms import StoreLocationForm
from locator.models import Locations
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def show_locator(request):
    locations = Locations.objects.all()
    context = {
        "user": request.user,
        "locations": locations
    }
    return render(request, 'locator.html', context)


def create_location_entry(request):
    form = StoreLocationForm(request.POST)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("locator:locator")
    else:
        form = StoreLocationForm()

    context = {'form': form}
    return render(request, "location_entry.html", context)

def delete_location(request, id):
    location = Locations.objects.get(pk = id)
    location.delete()
    return HttpResponseRedirect(reverse('locator:locator'))

def edit_location(request, id):
    location = Locations.objects.get(pk = id)

    form = StoreLocationForm(request.POST or None, instance=location)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('locator:locator'))

    context = {'form': form}
    return render(request, "edit_location.html", context)

# @csrf_exempt
# @require_POST
# def create_location_ajax(request):
#     store_name = request.POST.get("store_name")
#     street_name = request.POST.get("street_name")
#     district = request.POST.get("district")
#     gmaps_link = request.POST.get("gmaps_link")

#     new_location = Locations(
#         store_name=store_name, street_name=street_name,
#         district=district, gmaps_link=gmaps_link,
#     )
#     new_location.save()

#     return HttpResponse(b"CREATED", status=201)

def show_xml(request):
    data = Locations.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Locations.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")