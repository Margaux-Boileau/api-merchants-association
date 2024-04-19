# Generated by Django 5.0.3 on 2024-04-15 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_remove_post_id_forum'),
        ('shops', '0007_alter_shop_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shops.shop'),
        ),
    ]
