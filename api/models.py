from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.id}: {self.name}"

class Word(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    og = models.CharField(max_length=255)
    tr = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.id}: {self.og} - {self.tr} in {self.collection.name}"

class Context(models.Model):
    og = models.TextField()
    tr = models.TextField()
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id}: {self.og} - {self.tr}"
