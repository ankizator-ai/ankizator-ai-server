from djongo import models

class Source(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
