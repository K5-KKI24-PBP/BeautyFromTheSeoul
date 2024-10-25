# Generated by Django 5.1 on 2024-10-25 14:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("locator", "0002_rename_store_address_locations_street_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="locations",
            name="store_image",
            field=models.URLField(
                default="https://media.licdn.com/dms/image/D5612AQHir6Tb_Y0nCQ/article-cover_image-shrink_720_1280/0/1700275648664?e=2147483647&v=beta&t=-MICDezx6F8SIsfkj7yYM_1WCGiLeE-uxPAMbjZ4Byc",
                max_length=300,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="locations",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]