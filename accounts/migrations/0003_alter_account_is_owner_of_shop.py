# Generated by Django 5.0.3 on 2024-04-15 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_is_owner_of_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='is_owner_of_shop',
            field=models.BooleanField(default=False),
        ),
    ]
