# Generated by Django 3.2.23 on 2023-11-17 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycarsapp', '0003_alter_product_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.CharField(default='default_value', max_length=255),
        ),
    ]
