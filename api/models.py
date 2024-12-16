from django.contrib.auth.models import User
from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

class Example(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Word(models.Model):
    og = models.CharField(max_length=255)
    tr = models.CharField(max_length=255)
    example = models.ForeignKey(Example, on_delete=models.CASCADE, null=True)

class Context(models.Model):
    og = models.TextField()
    tr = models.TextField()
    example = models.ForeignKey(Example, on_delete=models.CASCADE)
