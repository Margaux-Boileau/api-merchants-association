# Generated by Django 5.0.3 on 2024-04-15 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0012_alter_forum_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='image',
        ),
    ]
