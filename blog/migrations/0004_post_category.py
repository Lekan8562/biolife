# Generated by Django 4.1.7 on 2023-11-13 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(default='Healthy Living', max_length=100),
        ),
    ]
