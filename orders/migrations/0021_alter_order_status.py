# Generated by Django 4.2.3 on 2023-07-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('complated', 'complated'), ('Accepted', 'Accepted'), ('New', 'New')], default='New', max_length=50),
        ),
    ]
