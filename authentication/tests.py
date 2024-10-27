from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from authentication.forms import RegistrationForm, CustomAuthenticationForm
from authentication.models import UserProfile

User = get_user_model()

class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='admin123', email='admin@example.com')

    def test_login_view_get(self):
        response = self.client.get(reverse('authentication:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_view_post_valid_credentials(self):
        response = self.client.post(reverse('authentication:login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('main:show_main'))
        self.assertIn('_auth_user_id', self.client.session)  

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(reverse('authentication:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Incorrect username or password. Please try again.")
    
    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('authentication:logout'))
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('main:show_main'))
        self.assertNotIn('_auth_user_id', self.client.session) 
    
    def test_register_view_get(self):
        response = self.client.get(reverse('authentication:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_valid(self):
        response = self.client.post(reverse('authentication:register'), {
            'username': 'newuser',
            'name': 'New User',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'user_role': 'customer'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('authentication:login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser', user_role='customer').exists())

    def test_register_view_post_duplicate_email(self):
        response = self.client.post(reverse('authentication:register'), {
            'username': 'anotheruser',
            'name': 'Another User',
            'email': 'testuser@example.com', 
            'password1': 'password123',
            'password2': 'password123',
            'user_role': 'customer'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This email is already in use.")
        self.assertFalse(User.objects.filter(username='anotheruser').exists())

    def test_custom_authentication_form_valid(self):
        form_data = {'username': 'testuser', 'password': 'password123'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_custom_authentication_form_invalid(self):
        form_data = {'username': 'testuser', 'password': 'wrongpassword'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_register_view_redirect_if_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('authentication:register'))
        self.assertRedirects(response, reverse('main:show_main'))
