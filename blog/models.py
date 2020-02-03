from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce.models import HTMLField

class Author(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
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
    overview = models.TextField()
    content = HTMLField('Content')
    timestamp = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    comment_count = models.IntegerField(default=0)
    featured = models.BooleanField()
    prev_post = models.ForeignKey(
        'self', related_name='previous_post', on_delete=models.SET_NULL, null=True, blank=True)
    nxt_post = models.ForeignKey(
        'self', related_name='next_post', on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        ordering = ['-timestamp', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})
        
    def get_update_url(self):
        return reverse('blog:post-update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('blog:post-delete', kwargs={'slug': self.slug})


    @property
    def get_comments(self):
        return self.comment_set.all()

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