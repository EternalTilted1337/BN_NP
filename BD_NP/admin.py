from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


admin.site.register(Category)
admin.site.register(Post)