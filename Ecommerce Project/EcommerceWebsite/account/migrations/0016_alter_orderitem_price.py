# Generated by Django 4.1.7 on 2023-03-03 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]