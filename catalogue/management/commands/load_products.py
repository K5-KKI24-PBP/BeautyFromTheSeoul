import json
from django.core.management.base import BaseCommand
from catalogue.models import Products

class Command(BaseCommand):
    help = 'Load products from a JSON file'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Products.objects.all().delete()

        with open('products.json', 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

            # Check if the data is a list or a single product
            if isinstance(data, list):
                products_data = data
            else:
                products_data = [data]  # Wrap in a list if it's a single item

            for item in products_data:
                if item['model'] == 'catalogue.Products':
                    fields = item['fields']
                    product_id = item['pk']

                    # Create a new product entry
                    Products.objects.create(
                        product_id=product_id,
                        product_name=fields.get('product_name', '')[:200],  
                        product_brand=fields.get('product_brand', '')[:200],  
                        price=fields.get('price', ''),
                        product_description=fields.get('product_description', '')[:200],  
                        product_type=fields.get('product_type', '')[:200],  
                        image=fields.get('image', '')[:200],  
                    )

        self.stdout.write(self.style.SUCCESS('Successfully loaded products'))
