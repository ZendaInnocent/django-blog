from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.slug




class Post(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    comment_count = models.IntegerField(default=0)
    featured = models.BooleanField()


    class Meta:
        ordering = ['-timestamp', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.body[:30]


class Gallery(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='gallery')

    class Meta:
        verbose_name_plural = 'Gallery'

    def __str__(self):
        return self.title