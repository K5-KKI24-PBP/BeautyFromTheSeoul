import calendar
from datetime import datetime
from functools import wraps
from django.shortcuts import get_object_or_404, render, redirect
from authentication.models import UserProfile
from events.models import Events, RSVP
from events.forms import EventsForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied. You must be a superuser to access this page.")
    return _wrapped_view

def show_events(request):
    return render(request, 'show_event.html')

@superuser_required
@login_required(login_url='authentication:login')
def create_event(request):
    if request.method == 'POST':
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:event')
    else:
        form = EventsForm()
    
    context = {
        'form': form
    }
    return render(request, 'create_event.html', context)

@superuser_required
@login_required(login_url='authentication:login')
def edit_event(request, id):
    event = Events.objects.get(id=id)
    if request.method == 'POST':
        form = EventsForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:event')
    else:
        form = EventsForm(instance=event)

    context = {
        'form': form
    }
    return render(request, 'edit_event.html', context)

@superuser_required
@login_required(login_url='authentication:login')
@csrf_exempt
def delete_event_ajax(request, id):
    try:
        event = Events.objects.get(id=id)
    except Events.DoesNotExist:
        return JsonResponse({'message': 'Event not found'}, status=404)

    event.delete()
    return JsonResponse({'message': 'Event deleted'})

@csrf_exempt
@login_required(login_url='authentication:login')
def rsvp_ajax(request, event_id):
    try:
        event = get_object_or_404(Events, id=event_id)
        user = get_object_or_404(User, username=request.user.username)
        user_profile = get_object_or_404(UserProfile, user=user)
    except:
        return JsonResponse({'message': 'User or event not found' }, status=404)

    rsvp, created = RSVP.objects.get_or_create(event=event, user=user_profile)
    rsvp.rsvp_status = True
    rsvp.save()

    data = {
        'message': 'RSVP successful',
        'rsvp_id': rsvp.id
    }
    return JsonResponse(data)

@csrf_exempt
@login_required(login_url='authentication:login')
def delete_rsvp_ajax(request, event_id):
    try:
        user = get_object_or_404(User, username=request.user.username)
        event = get_object_or_404(Events, id=event_id)
        user_profile = get_object_or_404(UserProfile, user=user)
    except:
        return JsonResponse({'message': 'User or event not found' }, status=404)

    rsvp = RSVP.objects.filter(event=event, user=user_profile).first()
    if rsvp:
        rsvp.delete()
        return JsonResponse({ 'message': 'RSVP deleted' })
    return JsonResponse({ 'message': 'RSVP not found' }, status=404)



def filter_events(request):
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')

    try:
        user = User.objects.get(username=request.user.username)
        user_profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        user_profile = None

    if month.isdigit() and year.isdigit():
        month = int(month)
        year = int(year)
        last_day = calendar.monthrange(year, month)[1]
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, last_day)
        events = Events.objects.filter(start_date__lte=end_date, end_date__gte=start_date)
    else:
        events = Events.objects.all()  

    if user_profile:
        rsvps = RSVP.objects.filter(event__in=events, user=user_profile) 
        rsvp_event_ids = [rsvp.event.id for rsvp in rsvps]

        rsvp_events = events.filter(id__in=rsvp_event_ids)
        non_rsvp_events = events.exclude(id__in=rsvp_event_ids)

        events = list(rsvp_events) + list(non_rsvp_events)
    else:
        rsvps = []
    
    return JsonResponse({
        'events': serializers.serialize('json', events),
        'rsvps': serializers.serialize('json', rsvps),
    }, safe=False)

def user_info(request):
    data = {
        'is_authenticated': request.user.is_authenticated,
        'is_superuser': request.user.is_superuser if request.user.is_authenticated else False,
    }

    return JsonResponse(data)

@superuser_required
@login_required(login_url='authentication:login')
def show_json_rsvp(request):
    data = RSVP.objects.all()
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )

@superuser_required
@login_required(login_url='authentication:login')
def show_json(request):
    events = Events.objects.all()
    data = serializers.serialize('json', events)
    return HttpResponse(data, content_type='application/json')