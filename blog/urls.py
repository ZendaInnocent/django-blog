from django.urls import path
from .views import (
    HomePageView, SearchResultsView, PostListView, PostDetailView,
    CategoryDetailView, 
)

app_name = 'blog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('blog/', PostListView.as_view(), name='post-list'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='post-category'),
    # path('contact/', ContactView.as_view(), name='contact'),
]