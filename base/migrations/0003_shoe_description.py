# Generated by Django 4.1.7 on 2023-03-05 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_shoe_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='description',
            field=models.TextField(default='A perfect shoe', max_length=50),
            preserve_default=False,
        ),
    ]