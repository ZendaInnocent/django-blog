from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Author, Comment, Gallery
from marketing.models import Subscriber
from django.db.models import Count, Q
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostCreateForm


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
        context['featured_posts'] = Post.objects.filter(featured=True)[:4]
        context['gallery_items'] = Gallery.objects.all()[:4]
        return context

    def post(self, request):
        if request.method == 'POST':
            email = request.POST['email']
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            
            if created:
                messages.success(request, 'Please check your e-mail for confirmation')
            elif subscriber:
                 messages.success(request, 'This email already in the list')
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
        context['comments'] = self.object.get_comments
        context['latest_posts'] = Post.objects.all()[:3]
        return context

    def post(self, request, **kwargs):
        if request.method == 'POST':
            post = Post.objects.get(slug=kwargs['slug'])
            author = request.user.username
            body = request.POST['usercomment']
            Comment.objects.create(post=post, author=author, body=body)
        return redirect('blog:post-detail', slug=kwargs['slug'])
    

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'overview', 'content', 'categories', 'thumbnail', 'featured']

    def form_valid(self, form):
        author = get_object_or_404(Author, user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return True
        return False

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'overview', 'content', 'categories', 'thumbnail', 'featured']

    def form_valid(self, form):
        author = get_object_or_404(Author, user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author.user:
            return True
        return False

    # def form_valid(self, form):
    #     form.instance.author = self.request.user.id
    #     action = self.request.POST.get('action')
    #     if action == 'SAVE':
    #         return super().form_valid(form)
    #     elif action == 'PREVIEW':
    #         preview = Post(
    #             title = form.cleaned_data['title'],
    #             slug = form.cleaned_data['slug'],
    #             author = form.cleaned_data['user'],
    #         )
    #         context = self.get_context_data(preview=preview)
    #         return self.render_to_response(context=context)
    #     return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post-list')

    def test_func(self):
        post = self.get_object()
        if post.author.user == self.request.user:
            return True
        return False


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'blog/post_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_count'] = get_category_count()
        context['latest_posts'] = Post.objects.all()[:3]
        return context