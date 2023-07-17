# Generated by Django 4.2.3 on 2023-07-14 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'), ('New', 'New'), ('complated', 'complated')], default='New', max_length=50),
        ),
    ]