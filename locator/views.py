from django.shortcuts import render, redirect
from locator.forms import StoreLocationForm
from locator.models import Locations

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