# Generated by Django 5.1.2 on 2024-11-22 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
