# Generated by Django 5.0.3 on 2024-03-18 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_owner_of_shop',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
