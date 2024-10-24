from django.shortcuts import render, redirect
from locator.forms import StoreLocationForm
from locator.models import Locations
from django.http import HttpResponse
from django.core import serializers

def show_locator(request):
    return render(request, 'locator.html')

def create_location_entry(request):
    form = StoreLocationForm(request.POST)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("locator:locator")
    else:
        form = StoreLocationForm()

    context = {'form': form}
    return render(request, "location_entry.html", context)

def show_xml(request):
    data = Locations.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Locations.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")