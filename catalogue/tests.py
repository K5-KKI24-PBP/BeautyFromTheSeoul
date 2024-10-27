from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalogue.models import Products, Review
from favorites.models import Favorite
from catalogue.forms import AddProductForm, ReviewForm

User = get_user_model()

class CatalogueTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')

        self.product = Products.objects.create(
            product_id='d69d832b-32a0-4f40-bc61-0ea736cca37c',
            product_name='VITALIFT-A',
            product_brand='Dr. Different',
            product_type='Other Spot Treatments',
            product_description='Night cream for anti-aging',
            price='5823.72',
            image='https://example.com/product.jpg'
        )

        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='Great product!'
        )

    def test_show_products_view(self):
        response = self.client.get(reverse('catalogue:show_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'VITALIFT-A')
    
    def test_product_filter_view(self):
        response = self.client.get(reverse('catalogue:filter_products_ajax'), {
            'product_brand': 'Dr. Different',
            'product_type': 'Other Spot Treatments'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'VITALIFT-A')

    def test_add_product_view(self):
        self.client.login(username='admin', password='admin123')
        
        response = self.client.post(reverse('catalogue:add_product_entry'), {
            'product_name': 'New Product',
            'product_brand': 'New Brand',
            'product_type': 'Moisturizer',
            'product_description': 'New product description',
            'price': '1999',
            'image': 'https://example.com/new-product.jpg'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Products.objects.filter(product_name='New Product').exists())

    def test_edit_product_view(self):
        self.client.login(username='admin', password='admin123')
        
        response = self.client.post(reverse('catalogue:edit_product', args=[self.product.product_id]), {
            'product_name': 'Updated VITALIFT-A',
            'product_brand': 'Updated Brand',
            'product_type': 'Essence',
            'product_description': 'Updated description',
            'price': '3000',
            'image': 'https://example.com/updated-product.jpg'
        })
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.product_name, 'Updated VITALIFT-A')
        self.assertEqual(response.status_code, 302)

    def test_delete_product_view(self):
        self.client.login(username='admin', password='admin123')
        
        response = self.client.post(reverse('catalogue:delete_product', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Products.objects.filter(product_id=self.product.product_id).exists())

    def test_add_favorite(self):
        self.client.login(username='testuser', password='password123')
        
        response = self.client.post(reverse('favorites:add_favorites', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'added': True})
        self.assertTrue(Favorite.objects.filter(user=self.user, skincare_product=self.product).exists())

    def test_remove_favorite(self):
        self.client.login(username='testuser', password='password123')
        Favorite.objects.create(user=self.user, skincare_product=self.product)
        
        response = self.client.post(reverse('favorites:remove_favorites', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Your favorite product has been removed from your favorites.'})
        self.assertFalse(Favorite.objects.filter(user=self.user, skincare_product=self.product).exists())

    def test_add_review(self):
        self.client.login(username='testuser', password='password123')
        
        response = self.client.post(reverse('catalogue:add_review', args=[self.product.product_id]), {
            'rating': 5,
            'comment': 'Excellent product!'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(user=self.user, product=self.product, rating=5).exists())

    def test_delete_review(self):
        self.client.login(username='admin', password='admin123')
        
        response = self.client.post(reverse('catalogue:delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_add_product_form_validation(self):
        form_data = {
            'product_name': '<b>Valid Product</b>',
            'product_brand': '<i>Valid Brand</i>',
            'product_type': '<script>Essence</script>',
            'product_description': 'Good for skin',
            'price': '<span>4999</span>',
            'image': 'https://example.com/valid-product.jpg',
        }
        form = AddProductForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data['product_name'], 'Valid Product')
        self.assertEqual(form.cleaned_data['product_brand'], 'Valid Brand')
        self.assertEqual(form.cleaned_data['product_type'], 'Essence')
        self.assertEqual(form.cleaned_data['price'], '4999')

    def test_review_form_validation(self):
        form_data = {
            'rating': '<b>5</b>',
            'comment': '<script>alert("bad")</script>Great product!'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['rating'], '5')
        self.assertEqual(form.cleaned_data['comment'], 'alert("bad")Great product!')
