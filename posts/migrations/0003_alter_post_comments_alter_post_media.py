# Generated by Django 5.0.3 on 2024-04-08 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
        ('posts', '0002_remove_post_id_forum_comment_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, to='posts.comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='media',
            field=models.ManyToManyField(blank=True, to='media.media'),
        ),
    ]
