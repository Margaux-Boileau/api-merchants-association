# Generated by Django 5.0.3 on 2024-04-18 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_is_owner_of_shop'),
        ('shops', '0013_alter_shop_facebook_alter_shop_instagram_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='shop_working_at',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shops.shop'),
        ),
    ]