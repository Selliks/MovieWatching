from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_set', blank=True
    )

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=124, unique=True)
    description = models.TextField(max_length=512)
    age = models.IntegerField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_of_post = models.DateTimeField(auto_now_add=True)
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.movie.title}'
