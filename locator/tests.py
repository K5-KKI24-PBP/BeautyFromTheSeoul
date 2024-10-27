from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from locator.models import Locations
from locator.forms import StoreLocationForm

class LocationsTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='password'
        )
        
        self.location = Locations.objects.create(
            store_name="Test Store",
            street_name="Test Street",
            district="Test District",
            gmaps_link="https://maps.google.com/?cid=1234567890",
            store_image="https://example.com/image.jpg"
        )

    def test_show_locator(self):
        response = self.client.get(reverse('locator:locator'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Store")

    def test_create_location_entry(self):
        self.client.login(username='admin', password='password')
        
        response = self.client.post(reverse('locator:location_entry'), {
            'store_name': 'New Store',
            'street_name': 'New Street',
            'district': 'New District',
            'gmaps_link': 'https://maps.google.com/?cid=9876543210',
            'store_image': 'https://example.com/new-image.jpg'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Locations.objects.filter(store_name='New Store').exists())

    def test_edit_location_entry(self):
        self.client.login(username='admin', password='password')
        
        response = self.client.post(reverse('locator:edit_location', args=[self.location.id]), {
            'store_name': 'Updated Store',
            'street_name': 'Updated Street',
            'district': 'Updated District',
            'gmaps_link': 'https://maps.google.com/?cid=1122334455',
            'store_image': 'https://example.com/updated-image.jpg'
        })
        
        self.location.refresh_from_db()
        self.assertEqual(self.location.store_name, 'Updated Store')
        self.assertEqual(self.location.gmaps_link, 'https://maps.google.com/?cid=1122334455')
        self.assertEqual(response.status_code, 302)

    def test_delete_location(self):
        self.client.login(username='admin', password='password')
        
        response = self.client.post(reverse('locator:delete_location', args=[self.location.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Locations.objects.filter(pk=self.location.id).exists())
    
    def test_filter_locations(self):
        Locations.objects.create(
            store_name="Another Store",
            street_name="Another Street",
            district="Different District",
            gmaps_link="https://maps.google.com/?cid=2233445566",
            store_image="https://example.com/another-image.jpg"
        )
        
        response = self.client.get(reverse('locator:filter_locations') + '?district=Test District')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Store")
        self.assertNotContains(response, "Another Store")

    def test_form_validity(self):
        form_data = {
            'store_name': 'Valid Store',
            'street_name': 'Valid Street',
            'district': 'Valid District',
            'gmaps_link': 'https://maps.google.com/?cid=9876543210',
            'store_image': 'https://example.com/valid-image.jpg',
        }
        form = StoreLocationForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data_invalid = {
            'store_name': 'Invalid Store',
            'street_name': 'Invalid Street',
            'district': 'Invalid District',
            'gmaps_link': '',  
            'store_image': 'https://example.com/invalid-image.jpg',
        }
        form_invalid = StoreLocationForm(data=form_data_invalid)
        self.assertFalse(form_invalid.is_valid())
