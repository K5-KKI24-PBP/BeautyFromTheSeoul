from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import AdEntry
from main.forms import AdForm

class AdEntryTests(TestCase):

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
        
        self.ad = AdEntry.objects.create(
            brand_name="Test Brand",
            image="https://example.com/image.jpg",
            is_approved=False
        )

    def test_show_main_as_staff(self):
        self.client.login(username='admin', password='password')
        
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Brand")
    
    def test_show_main_as_regular_user(self):
        self.client.login(username='user', password='password')
        
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Brand")

    def test_create_ad_post(self):
        self.client.login(username='user', password='password')
        
        response = self.client.post(reverse('main:create_ad'), {
            'brand_name': 'New Brand',
            'image': 'https://example.com/new-image.jpg'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(AdEntry.objects.filter(brand_name='New Brand').exists())

    def test_edit_ad_post(self):
        self.client.login(username='admin', password='password')
        
        response = self.client.post(reverse('main:edit_ad', args=[self.ad.id]), {
            'brand_name': 'Updated Brand',
            'image': 'https://example.com/updated-image.jpg'
        })
        
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.brand_name, 'Updated Brand')
        self.assertEqual(self.ad.image, 'https://example.com/updated-image.jpg')
        
        self.assertEqual(response.status_code, 302)

    def test_delete_ad(self):
        self.client.login(username='admin', password='password')
        
        response = self.client.post(reverse('main:delete_ad', args=[self.ad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(AdEntry.objects.filter(pk=self.ad.id).exists())
    
    def test_approve_ad_as_staff(self):
        self.client.login(username='admin', password='password')
        
        response = self.client.post(reverse('main:approve_ad', args=[self.ad.id]))
        
        self.ad.refresh_from_db()
        self.assertTrue(self.ad.is_approved)
        self.assertEqual(response.status_code, 302)
    
    def test_form_validity(self):
        form_data = {
            'brand_name': 'Valid Brand',
            'image': 'https://example.com/image.jpg',
        }
        form = AdForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data_invalid = {
            'brand_name': 'Invalid Brand',
            'image': '', 
        }
        form_invalid = AdForm(data=form_data_invalid)
        self.assertFalse(form_invalid.is_valid())