# Generated by Django 5.0.1 on 2024-01-06 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=1, upload_to='categories_images'),
            preserve_default=False,
        ),
    ]
