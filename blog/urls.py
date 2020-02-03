from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('blog/', views.PostListView.as_view(), name='post-list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('search/', views.SearchResultsView.as_view(), name='search-results'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='post-category'),
    path('post-create/', views.PostCreateView.as_view(), name='post-create'),
    # path('contact/', ContactView.as_view(), name='contact'),
]