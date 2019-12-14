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

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=140)
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
        return reverse('blog:post-detail', kwargs={'pk': self.id})