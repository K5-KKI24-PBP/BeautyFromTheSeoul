import json
from django.core.management.base import BaseCommand
from catalogue.models import Products

class Command(BaseCommand):
    help = 'Load products from a JSON file'

    def handle(self, *args, **kwargs):
        # Open and read the JSON file
        with open('products.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            product_list = []

            # Iterate over each product and create a Product instance with truncated fields
            for item in data:
                fields = item['fields']
                
                # Truncate string fields to 200 characters if needed
                product_name = fields['product_name'][:200]
                product_brand = fields['product_brand'][:200]
                product_description = fields['product_description'][:200]
                product_type = fields['product_type'][:200]
                image = fields['image'][:200]  # Truncate the image URL if necessary
                
                # Create a Product object with the truncated fields
                product_list.append(Products(
                    product_id=fields['product_id'],
                    product_name=product_name,
                    product_brand=product_brand,
                    price=fields['price'],
                    product_description=product_description,
                    product_type=product_type,
                    image=image
                ))

            # Use bulk_create for batch insertion to optimize performance
            from django.db import transaction
            with transaction.atomic():
                Products.objects.bulk_create(product_list)

        # Notify success
        self.stdout.write(self.style.SUCCESS('Successfully loaded products'))
