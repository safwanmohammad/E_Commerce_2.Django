# Generated by Django 4.2.3 on 2023-07-14 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('complated', 'complated'), ('New', 'New'), ('Cancelled', 'Cancelled')], default='New', max_length=50),
        ),
    ]
