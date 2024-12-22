from django.shortcuts import render, redirect, reverse, get_object_or_404
from locator.forms import StoreLocationForm
from locator.models import Locations
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

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

    data = serializers.serialize('json', locations)
    
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

@csrf_exempt
def create_location_flutter(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            print(data)
            
            # Extract fields from the request
            store_name = data.get('storeName')
            street_name = data.get('streetName')
            district = data.get('district')
            gmaps_link = data.get('gmapsLink')
            store_image = data.get('storeImage')

            # Validate required fields
            if not all([store_name, street_name, district, gmaps_link, store_image]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Create a new Location object
            location = Locations.objects.create(
                store_name=store_name,
                street_name=street_name,
                district=district,
                gmaps_link=gmaps_link,
                store_image=store_image
            )

            # Respond with success
            return JsonResponse({
                'message': 'Location created successfully',
                'location_id': location.id
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def edit_location_flutter(request, id):
    if request.method == "POST":
        try:
            location = get_object_or_404(Locations, pk=id)
            data = json.loads(request.body)

            # Manually update the instance with the data from the request body
            store_name = data.get('store_name')
            street_name = data.get('street_name')
            district = data.get('district')
            gmaps_link = data.get('gmaps_link')
            store_image = data.get('store_image')

            # Update the fields individually
            location.store_name = store_name
            location.street_name = street_name
            location.district = district
            location.gmaps_link = gmaps_link
            location.store_image = store_image

            # Save the updated location
            location.save()

            # Update the instance with new data
            form = StoreLocationForm(data, instance=location)

            if form.is_valid():
                form.save()
                return JsonResponse({
                    "success": True,
                    "message": "Location updated successfully",
                    "location": {
                        "id": location.id,
                        "storeName": location.store_name,
                        "streetName": location.street_name,
                        "district": location.district,
                        "gmapsLink": location.gmaps_link,
                        "storeImage": location.store_image,
                    }
                }, status=200)
            else:
                return JsonResponse({
                    "success": False,
                    "message": "Invalid data",
                    "errors": form.errors,
                }, status=400)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }, status=500)
        
    return JsonResponse({
        "success": False,
        "message": "Method not allowed"
    }, status=405)

@csrf_exempt
def fetch_locations(request):
    if request.method == "GET":
        locations = Locations.objects.all()  # Fetch all locations
        location_list = [
            {
                "id": location.id,
                "storeName": location.store_name,
                "streetName": location.street_name,
                "district": location.district,
                "gmapsLink": location.gmaps_link,
                "storeImage": location.store_image,
            }
            for location in locations
        ]
        print(location_list)
        return JsonResponse({"locations": location_list}, safe=False, status=200)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def delete_location_flutter(request, id):
    if request.method == "DELETE":
        try:
            # Get the location object or return 404 if not found
            location = get_object_or_404(Locations, pk=id)
            location.delete()  # Delete the location object

            return JsonResponse({
                "success": True,
                "message": "Location deleted successfully",
            }, status=200)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }, status=500)
    else:
        return JsonResponse({
            "success": False,
            "message": "Invalid request method"
        }, status=400)