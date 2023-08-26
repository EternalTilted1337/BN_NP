from django.contrib.auth.models import User
from BD_NP.models import Author, Category, Post, Comment, User

# создать пользователей
user1 = User.objects.create_user('john')
user2 = User.objects.create_user('mary')
#++++++++++++++++++++++++++++++++++++++++

# создать авторов
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)
#+

# создать категории
category1 = Category.objects.create(name='IT')
category2 = Category.objects.create(name='Sport')
category3 = Category.objects.create(name='Lifestyle')
category4 = Category.objects.create(name='Science')
#+

# создать посты
post1 = Post.objects.create(author=author1, title='Python tutorial', text='Learn Python')
post2 = Post.objects.create(author=author2, title='Yoga for beginners', text='Yoga tips...')
#+

# назначить категории
post1.categories.add(category1, category4)
post2.categories.add(category2, category3)
#?

# создать комментарии
Comment.objects.create(post=post1, user=user2, text='Useful tutorial!')
Comment.objects.create(post=post1, user=user1, text='Thanks, helped me!')
Comment.objects.create(post=post2, user=user2, text='Very informative')
Comment.objects.create(post=post2, user=user1, text='Nice tips for yoga')


# лайкнуть и дизлайкнуть
post1.like()
post2.dislike()
post2.comment_set.first().like()
#post2.comment_set.first().like() вставить

# обновить рейтинги
author1.update_rating()
author2.update_rating()

# вывести лучшего автора
print(Author.objects.order_by('-rating').first().user.username)

# вывести лучший пост
best_post = Post.objects.order_by('-rating').first()
print(best_post.created_at, best_post.author.user.username, best_post.rating, best_post.title, best_post.preview())

# вывести комментарии к лучшему посту
for c in best_post.comment_set.all():
    print(c.created_at, c.user.username, c.rating, c.text)