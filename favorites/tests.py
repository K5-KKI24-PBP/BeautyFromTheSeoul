from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Favorite, Products
from catalogue.models import Review

User = get_user_model()

class FavoritesViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Products.objects.create(
            product_id='d69d832b-32a0-4f40-bc61-0ea736cca37c',
            product_name='VITALIFT-A',
            product_brand='Dr. Different',
            product_description='This night-time skin treatment is ideal for those looking to improve the appearance of aging skin.The main ingredient: Retinal brings similar results of smoothing fine lines and wrinkles as retinol through stimulating collagen production, but has been proven to work faster than its counterpart. In addition, retinal is more efficient at exfoliating, contributing to brighter skin and more even tone.Other ingredients: Hyaluronic acid is a favorite for plumping and hydrating, which helps skin appear smoother and more radiant. Safflower oil is an anti-inflammatory ingredient that helps calm irritation and protect skin from damage. The result is more youthful, supple skin.pH of 6.50-8.50. Formulated without artificial fragrances and colors, parabens, sulfates, animal products, mineral oil, essential oil, alcohol, and silicone.0.7 oz./ 20gn',
            price='\u20a958323.72',
            product_type='Other Spot Treatments',
            image='https://web.tradekorea.com/product/449/2039449/VITALIFT-A_NIGHT_CREAM_2.png'
        )

    def test_show_favorites_not_logged_in(self):
        response = self.client.get(reverse('favorites:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'not_logged_in.html')

    def test_show_favorites_logged_in_empty(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('favorites:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['favorites']), [])
    
    def test_add_favorites(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('favorites:add_favorites', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'added': True})

        self.assertTrue(Favorite.objects.filter(user=self.user, skincare_product=self.product).exists())
    
    def test_add_favorites_already_exists(self):
        self.client.login(username='testuser', password='password123')
        self.client.post(reverse('favorites:add_favorites', args=[self.product.product_id]))
        response = self.client.post(reverse('favorites:add_favorites', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'removed': True})

        self.assertFalse(Favorite.objects.filter(user=self.user, skincare_product=self.product).exists())
    
    def test_remove_favorites(self):
        self.client.login(username='testuser', password='password123')
        self.client.post(reverse('favorites:add_favorites', args=[self.product.product_id]))

        response = self.client.post(reverse('favorites:remove_favorites', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Your favorite product has been removed from your favorites.'})

        self.assertFalse(Favorite.objects.filter(user=self.user, skincare_product=self.product).exists())
    
    def test_remove_favorites_not_in_list(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('favorites:remove_favorites', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'message': 'The following product is not in your favorites.'})