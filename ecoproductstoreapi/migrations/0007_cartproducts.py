# Generated by Django 4.2.7 on 2024-07-31 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecoproductstoreapi', '0006_remove_cart_product_remove_cart_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecoproductstoreapi.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecoproductstoreapi.product')),
            ],
        ),
    ]
