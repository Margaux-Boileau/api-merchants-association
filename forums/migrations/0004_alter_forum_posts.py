# Generated by Django 5.0.3 on 2024-04-08 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0003_remove_forum_shops_members_forum_read_members_and_more'),
        ('posts', '0002_remove_post_id_forum_comment_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='posts',
            field=models.ManyToManyField(null=True, to='posts.post'),
        ),
    ]