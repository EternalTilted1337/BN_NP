from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.crypto import get_random_string


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_ratings = self.post_set.aggregate(total_rating=Sum('rating'))
        self.rating = post_ratings['total_rating']
        self.save()

    def create(self, username=None, **kwargs):
        if not username:
            username = get_random_string(length=8)
        author = self(username=username, **kwargs)
        author.save()
        return author
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    #updated_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        ordering = ['created_at']