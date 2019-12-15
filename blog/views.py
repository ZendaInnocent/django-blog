from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Author, Comment, Gallery
from marketing.models import Subscriber
from django.db.models import Count, Q
from django.views.generic import ListView, DetailView, FormView
from django.contrib import messages
from django.urls import reverse_lazy


def get_category_count():
    categories = Category.objects.all().annotate(posts_count=Count('post'))
    return categories


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q' or None)
        if query:
            object_list = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )
            return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_count'] = get_category_count()
        return context


class HomePageView(ListView):
    queryset = Post.objects.all()[:3]
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(featured=True)
        context['gallery_items'] = Gallery.objects.all()[:4]
        return context

    def post(self, request):
        if request.method == 'POST':
            email = request.POST['email']
            Subscriber.objects.create(email=email)
            messages.success(request, 'Check your e-mail for confirmation')
        return super().get(request)

            


class PostListView(ListView):
    model = Post
    paginate_by = 4
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_count'] = get_category_count()
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_count'] = get_category_count()
        return context
    

class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'blog/post_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_count'] = get_category_count()
        return context