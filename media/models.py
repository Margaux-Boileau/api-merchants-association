from django.db import models

class Media(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
 