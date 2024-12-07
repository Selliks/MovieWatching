from django.db import models


class Movie(models.Model):
    title = models.CharField(unique=True, max_length=124)
    description = models.TextField(blank=False, max_length=512)
    age = models.IntegerField()
    genre = models.
    author = models.
    comment = models.
    date_of_post = models.DateTimeField()