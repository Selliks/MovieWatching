from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=512)
    age = models.IntegerField()
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    author = models.CharField(max_length=128)
    date_of_post = models.DateTimeField(auto_now_add=True)
    release_date = models.DateField(blank=True, null=True)
    preview_image = models.ImageField(upload_to='movie/previews/', blank=True, null=True)
    video_file = models.FileField(upload_to='movie/videos/', blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.movie.title}'
