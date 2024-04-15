from django.db import models

class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    image = models.ForeignKey('media.Media', on_delete=models.CASCADE, blank=True)
    read_members = models.ManyToManyField('shops.Shop', related_name='read_members')
    read_write_members = models.ManyToManyField('shops.Shop', related_name='read_write_members')
    posts = models.ManyToManyField('posts.Post', blank=True)