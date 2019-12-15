from django.contrib import admin
from .models import Category, Post, Author, Comment, Gallery


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Gallery)
