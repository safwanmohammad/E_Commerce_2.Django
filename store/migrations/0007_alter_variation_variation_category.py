# Generated by Django 4.2.3 on 2023-07-15 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_productgallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('Dimensions', 'Dimensions'), ('Type', 'Type')], max_length=100),
        ),
    ]