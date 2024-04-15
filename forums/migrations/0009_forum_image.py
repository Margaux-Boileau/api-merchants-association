# Generated by Django 5.0.3 on 2024-04-10 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0008_remove_forum_image'),
        ('media', '0003_media_id_alter_media_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='media.media'),
        ),
    ]
