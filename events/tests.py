from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import UserProfile
from events.models import Events, RSVP
from datetime import date
import json

class EventsTests(TestCase):
    
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')
        self.user = User.objects.create_user(username='user', password='userpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)

        self.event = Events.objects.create(
            name="Sample Event",
            description="This is a sample event",
            start_date=date.today(),
            end_date=date.today(),
            location="Seoul",
            promotion_type="Discount"
        )

        self.client = Client()

    def test_create_event_as_superuser(self):
        self.client.login(username='admin', password='adminpassword')

        response = self.client.post(reverse('events:create_event'), {
            'name': 'New Event',
            'description': 'New event description',
            'start_date': '2025-01-01',
            'end_date': '2025-01-02',
            'location': 'New York',
            'promotion_type': 'Sale'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Events.objects.filter(name='New Event').exists())

    def test_edit_event_as_superuser(self):
        self.client.login(username='admin', password='adminpassword')

        response = self.client.post(reverse('events:edit_event', args=[self.event.id]), {
            'name': 'Updated Event Name',
            'description': 'Updated description',
            'start_date': self.event.start_date,
            'end_date': self.event.end_date,
            'location': self.event.location,
            'promotion_type': self.event.promotion_type
        })
        
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, 'Updated Event Name')

    def test_delete_event_ajax(self):
        self.client.login(username='admin', password='adminpassword')

        response = self.client.post(reverse('events:delete_event_ajax', args=[self.event.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'Event deleted')
        self.assertFalse(Events.objects.filter(id=self.event.id).exists())

    def test_rsvp_event(self):
        self.client.login(username='user', password='userpassword')

        response = self.client.post(reverse('events:rsvp_ajax', args=[self.event.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        rsvp = RSVP.objects.filter(event=self.event, user=self.user_profile).first()
        self.assertIsNotNone(rsvp)
        self.assertTrue(rsvp.rsvp_status)
        self.assertEqual(json.loads(response.content)['message'], 'RSVP successful')

    def test_cancel_rsvp_event(self):
        rsvp = RSVP.objects.create(event=self.event, user=self.user_profile, rsvp_status=True)

        self.client.login(username='user', password='userpassword')

        response = self.client.post(reverse('events:delete_ajax', args=[self.event.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(RSVP.objects.filter(event=self.event, user=self.user_profile).exists())
        self.assertEqual(json.loads(response.content)['message'], 'RSVP deleted')
