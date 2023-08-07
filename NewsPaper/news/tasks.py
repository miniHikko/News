import datetime

from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .forms import NewsForm
from .models import Post, Category
from django.conf import settings


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i + 1)


@shared_task
def _news():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(data_time__gte=last_week)
    categorys = set(posts.values_list('category__subjiect', flat=True))
    subscribers = set(Category.objects.filter(subjiect__in=categorys).values_list('subscribers__email', flat=True))
    html_content = render_to_string('subsub.html', {'posts': posts, 'link': settings.SITE_URL})
    msg = EmailMultiAlternatives(
        subject='статьи за неделю',
        body="",
        from_email='mrmolocko@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()
