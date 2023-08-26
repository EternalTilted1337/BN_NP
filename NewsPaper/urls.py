"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BD_NP.views import NewsDetailView, NewsListView, news_list
from BD_NP.views import NewsCreateView, NewsUpdateView, NewsDeleteView
from BD_NP.views import ArticleCreateView, ArticleUpdateView, ArticleDeleteView
from django.urls import include


urlpatterns = [
    path('news/', NewsListView.as_view()), #работает
    path('news/<int:pk>/', NewsDetailView.as_view()),
    path('news/create/', NewsCreateView.as_view(), name='news_create'), #news_create.html | работает
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),#news_edit.html | работает
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'), #news_delete.html | работает
#Articles все работают
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'), #articles/create.html
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),#article_edit.html
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'), #article_delete.html
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    # path('', include('protect.urls')),
    # path('sign/', include('sign.urls')),
    # path('accounts/', include('allauth.urls')),
]

