from django.db import models

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    sector = models.CharField(max_length=255, null=True)
    image = models.ForeignKey('media.Media', on_delete=models.CASCADE, blank=True)
    workers = models.ManyToManyField('accounts.Account')
