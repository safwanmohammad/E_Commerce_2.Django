# Generated by Django 4.2.2 on 2023-07-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Cancelled', 'Cancelled'), ('Accepted', 'Accepted'), ('complated', 'complated')], default='New', max_length=50),
        ),
    ]
