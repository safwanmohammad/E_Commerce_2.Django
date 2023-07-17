# Generated by Django 4.2.3 on 2023-07-15 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('complated', 'complated'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled')], default='New', max_length=50),
        ),
    ]
