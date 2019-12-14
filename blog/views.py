from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Author, Comment
from django.db.models import Count


def get_category_count():
    categories = Category.objects.all().annotate(posts_count=Count('post'))
    return categories


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

    category_count = get_category_count()
    context = {
        'posts': posts,
        'category_count': category_count
    }
    return render(request, 'blog.html', context)


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        author = request.POST['username']
        body = request.POST['usercomment']

        new_comment = Comment(post=post, author=author, body=body)
        new_comment.save()

    comments = Comment.objects.filter(post=post)

    category_count = get_category_count()
 
    context = {
        'post': post,
        'comments': comments,
        'category_count': category_count
    }
    return render(request, 'post.html', context)