from django.urls import path
from .views import index, blog, post

app_name = 'blog'

urlpatterns = [
    path('', index, name='home'),
    path('blog/', blog, name='post-list'),
    path('post/<int:post_id>/', post, name='post-detail'),
]