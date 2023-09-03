from django.views.generic import ListView
from BD_NP.models import Post , Appointment, Category, models
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from datetime import datetime

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import Appointment

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
    template_name = 'create/create.html'


class NewsUpdateView(UpdateView): #Обновление новостей
  model = Post
  fields = ['title', 'text']
  template_name = 'news_edit.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['content_type'] = 'protect'
    return context


class NewsDeleteView(DeleteView): #Удаление новостей
    model = Post
    template_name = 'news_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_type'] = 'protect'
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

@login_required
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

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

class ProtectedView(TemplateView):
    template_name = 'main.html',


class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'



class CustomLoginView(LoginView):
    template_name = 'login.html'  # указывает на ваш шаблон формы входа
    success_url = '/home/'  # URL, куда будет перенаправлен пользователь после успешного входа

    def form_valid(self, form):
        # Дополнительная логика, которую вы можете добавить при успешном входе
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'

    def dispatch(self, request, *args, **kwargs):
        # Дополнительная логика перед выходом пользователя
        # Например, отправка уведомления администратору или сохранение данных

        return super().dispatch(request, *args, **kwargs)

class CustomCategoryView(LogoutView):
    model = Category
    template_name = 'category.html'
    name = models.CharField(max_length=100)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
def subscribe_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.is_subscribed = not category.is_subscribed
    category.save()
    return redirect('category')


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='EternalTilted1337@yandex.ru',
            to=['skavik46111@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

        return redirect('appointments:make_appointment')