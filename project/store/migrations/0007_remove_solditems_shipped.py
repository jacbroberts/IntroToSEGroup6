# Generated by Django 5.1.2 on 2024-11-15 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_merge_0005_product_image_0005_solditems_shipped'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solditems',
            name='shipped',
        ),
    ]
