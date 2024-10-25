from functools import wraps
import json
from django.shortcuts import get_object_or_404, render, redirect
from authentication.models import UserProfile
from events.models import Events, RSVP
from events.forms import EventsForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied. You must be a superuser to access this page.")
    return _wrapped_view

def show_events(request):
    events = Events.objects.all()
    events = events.order_by('start_date')
    context = {
        'events': events
    }
    return render(request, 'show_event.html', context)

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
def delete_event(request, id):
    event = Events.objects.get(id=id)
    event.delete()

    return redirect('events:event')

@login_required(login_url='authentication:login')
def rsvp_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    rsvp, created = RSVP.objects.get_or_create(event=event, user=user_profile)
    rsvp.rsvp_status = True
    rsvp.save()
    return redirect('events:event')

@login_required(login_url='authentication:login')
def delete_rsvp(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    rsvp, created = RSVP.objects.get_or_create(event=event, user=user_profile)
    rsvp.delete()
    return redirect('events:event')

def show_json(request):
    events = Events.objects.all()
    data = {
        'events': list(events.values())
    }
    return JsonResponse(data)

def show_json_rsvp(request):
    data = RSVP.objects.all()
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )