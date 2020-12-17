from django.db import models

# Create your models here.

class Publisher(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    addr = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=32, unique=True)
    pub = models.ForeignKey('Publisher', on_delete=models.CASCADE)

class Author(models.Model):
    name = models.CharField(max_length=32)
    books = models.ManyToManyField('Book')