from django.db import models

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    sector = models.CharField(max_length=255, blank=True)
    instagram = models.URLField(blank=True, default=None, null=True)
    facebook = models.URLField(blank=True, default=None, null=True)
    webpage = models.URLField(blank=True, default=None, null=True)
    image = models.ForeignKey('media.Media', on_delete=models.DO_NOTHING, null=True, blank=True)
    workers = models.ManyToManyField('accounts.Account')