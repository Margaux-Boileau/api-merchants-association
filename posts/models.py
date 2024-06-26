import datetime
from django.db import models

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)
    body = models.CharField(max_length=255)
    media = models.ManyToManyField('media.Media', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    id_creator = models.ForeignKey('shops.Shop', on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey('shops.Shop', on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)