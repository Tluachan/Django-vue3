# Generated by Django 4.1 on 2023-03-17 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_category_thumbnail_alter_category_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='thumbnail',
            new_name='image',
        ),
    ]
