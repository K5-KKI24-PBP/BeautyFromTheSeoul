from django.shortcuts import render, redirect, reverse
from locator.forms import StoreLocationForm
from locator.models import Locations
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def show_locator(request):
    locations = Locations.objects.all()
    districts = Locations.objects.values_list('district', flat=True).distinct()
    context = {
        "user": request.user,
        "locations": locations,
        "districts": districts
    }
    return render(request, 'locator.html', context)

def filter_locations(request):
    district = request.GET.get('district', '')
    if district:
        locations = Locations.objects.filter(district=district)
    else:
        locations = Locations.objects.all()

    print("Filtered locations:", locations)  # Debugging print statement
    data = serializers.serialize('json', locations)
    print("Serialized data:", data)  # Debugging print statement
    return JsonResponse(data, safe=False)



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

def show_xml(request):
    data = Locations.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Locations.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")