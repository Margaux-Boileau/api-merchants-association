# Generated by Django 5.0.3 on 2024-04-13 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0004_remove_media_url_media_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='image',
        ),
        migrations.AlterField(
            model_name='media',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
