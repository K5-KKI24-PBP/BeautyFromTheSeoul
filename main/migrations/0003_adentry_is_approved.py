# Generated by Django 5.1 on 2024-10-24 02:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_alter_adentry_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="adentry",
            name="is_approved",
            field=models.BooleanField(default=False),
        ),
    ]