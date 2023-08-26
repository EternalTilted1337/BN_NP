from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_ratings = self.post_set.aggregate(total_rating=Sum('rating'))
        self.rating = post_ratings['total_rating']
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:124] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
        author = Author.objects.get(id=1)
        author.update_rating()

        post = Post.objects.get(id=1)
        post.like()
        post.dislike()
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

    def update_rating(self):
        post_ratings = self.post_set.aggregate(total_post_rating=Sum('rating'))
        comment_ratings = self.comment_set.aggregate(total_comment_rating=Sum('rating'))

        total_rating = post_ratings['total_post_rating'] + comment_ratings['total_comment_rating']

        self.rating = total_rating
        self.save()