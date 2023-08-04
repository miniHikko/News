from django.template.defaultfilters import upper
from django.urls import path, include
# Импортируем созданное нами представление
from .views import NewsList, NewDetail, create_new, news_search, NewDelete, NewUpdate, Author_make, category_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewDetail.as_view(), name="details"),
    path('search/', news_search.as_view()),
    path('smi/create/', create_new, name='news_create'),
    path('article/create', create_new, name='article_create'),
    path('<int:pk>/smi/update/', NewUpdate.as_view(), name='news_update'),
    path('<int:pk>/article/update/', NewUpdate.as_view(), name='news_update'),
    path('<int:pk>/smi/delete/', NewDelete.as_view(), name='news_delete'),
    path('<int:pk>/article/delete/', NewDelete.as_view(), name='news_delete'),
    path('make/', Author_make, name='make'),
    path('categories/<int:pk>/', category_view, name='categorys'),

]
