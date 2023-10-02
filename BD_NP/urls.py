from BD_NP.views import NewsDetailView, NewsListView, news_list, AppointmentView
from BD_NP.views import NewsCreateView, NewsUpdateView, NewsDeleteView
from BD_NP.views import ArticleCreateView, ArticleUpdateView, ArticleDeleteView
from django.urls import path
from BD_NP.views import IndexView, ProtectedView,subscribe_category, TemplateView, LoginRequiredMixin, CustomLoginView, CustomLogoutView, CustomCategoryView


urlpatterns = [
    path('', NewsListView.as_view()), #работает
    path('<int:pk>/', NewsDetailView.as_view()),
    path('create/', NewsCreateView.as_view(), name='news_create'), #news_create.html | работает
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),#news_edit.html | работает
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'), #news_delete.html | работает
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'), #articles/create.html
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),#article_edit.html
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('', IndexView.as_view()),
    path('account/', ProtectedView.as_view(), name='account'),
    path('sign/', ProtectedView.as_view(), name='sign'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('category/', CustomCategoryView.as_view(), name='category'),
    path('category/', CustomCategoryView.as_view(), name='category'),
    path('category/<int:category_id>/subscribe/', subscribe_category, name='subscribe_category'),
    path('appointment/', AppointmentView.as_view(), name='appointment'),
]