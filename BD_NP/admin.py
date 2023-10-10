from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, Appointment

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Appointment)