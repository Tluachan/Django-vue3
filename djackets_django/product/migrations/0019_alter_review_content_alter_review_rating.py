# Generated by Django 4.1 on 2023-03-20 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_remove_favoriteshop_shop_id_favoriteshop_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
