from django import forms
from django.contrib.auth import get_user_model

from .models import Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('comment_count', 'author', )

    
        