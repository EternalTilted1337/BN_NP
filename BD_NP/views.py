from django.views.generic import ListView
from BD_NP.models import Post
from django.views.generic.detail import DetailView
from django.shortcuts import render
from datetime import datetime
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'object'
    queryset = Post.objects.order_by('-id')
    paginate_by = 1 # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_param = self.request.GET.get('filter')

        if filter_param:
            queryset = queryset.filter(
                Q(title__icontains=filter_param) |
                Q(text__icontains=filter_param)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter')
        return context


def news_list(request):
    articles = Post.objects.order_by('-date')
    total_news_count = articles.count()
    return render(request, 'news_list.html', {'articles': articles, 'total_news_count': total_news_count})

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'
    pk_url_kwarg = 'pk'




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context
    ###################################################################################################
class NewsCreateView(CreateView): #Создание новости
    model = Post
    fields = ['title', 'text']
    template_name = 'news/create.html'


class NewsUpdateView(UpdateView): #Обновление новостей
  model = Post
  fields = ['title', 'text']
  template_name = 'news_edit.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['content_type'] = 'news'
    return context


class NewsDeleteView(DeleteView): #Удаление новостей
    model = Post
    template_name = 'news_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_type'] = 'news'
        return context

class PostCreateView(CreateView):
  model = Post
  fields = ['title', 'text']


class ArticleUpdateView(UpdateView): #Обновление статьи
    model = Post
    fields = ['title', 'text']
    template_name = 'article_edit.html'

class ArticleCreateView(PostCreateView): #Создание статьи
    temoplate_name = 'articles/create.html'

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['content_type'] = 'article'
    return context

class ArticleDeleteView(DeleteView): #Удаление статьи
    model = Post
    template_name = 'article_delete.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
  model = Post
  fields = ['name', 'avatar']
  template_name = 'edit_profile.html'

  def get_object(self):
    return self.request.user.profile

@receiver(post_save, sender=User) #
def user_saved(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get(name='common')
        instance.groups.add(common_group)
#геге