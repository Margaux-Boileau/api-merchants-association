# Generated by Django 5.0.3 on 2024-04-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0004_alter_forum_posts'),
        ('posts', '0002_remove_post_id_forum_comment_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='posts',
            field=models.ManyToManyField(to='posts.post'),
        ),
    ]