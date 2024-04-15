# Generated by Django 5.0.3 on 2024-04-08 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0002_forum_date_forum_posts'),
        ('shops', '0003_alter_shop_sector'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='shops_members',
        ),
        migrations.AddField(
            model_name='forum',
            name='read_members',
            field=models.ManyToManyField(related_name='read_members', to='shops.shop'),
        ),
        migrations.AddField(
            model_name='forum',
            name='read_write_members',
            field=models.ManyToManyField(related_name='read_write_members', to='shops.shop'),
        ),
    ]
