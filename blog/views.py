from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Author

def index(request):
    featured_posts = Post.objects.filter(featured=True)[:3]
    latest_posts = Post.objects.all()[:3]
    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts,
    }
    return render(request, 'index.html', context)


def blog(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog.html', context)


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post
    }
    return render(request, 'post.html', context)