# Generated by Django 4.1.7 on 2023-11-03 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_orderitem_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='colour',
        ),
        migrations.DeleteModel(
            name='Colour',
        ),
    ]
