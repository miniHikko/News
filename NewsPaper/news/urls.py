from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewDetail, create_new, news_search, NewDelete, NewUpdate

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', NewsList.as_view()),
    path('<int:pk>', NewDetail.as_view()),
    path('search/', news_search.as_view()),
    path('smi/create/', create_new, name='news_create'),
    path('article/create', create_new, name='article_create'),
    path('<int:pk>/smi/update/', NewUpdate.as_view(), name='news_update'),
    path('<int:pk>/article/update/', NewUpdate.as_view(), name='news_update'),
    path('<int:pk>/smi/delete/', NewDelete.as_view(), name='news_delete'),
    path('<int:pk>/article/delete/', NewDelete.as_view(), name='news_delete'),
]
