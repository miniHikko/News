from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView, CreateView
from .models import Post, Category
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.decorators import permission_required
from django.core.mail import EmailMultiAlternatives
from .tasks import hello, printer, _news
from django.core.cache import cache
import logging
logger = logging.getLogger('django.template')


class NewsList(LoginRequiredMixin, ListView):
    logger.error('dfjfjpodjfpojfpojdfpofpo[fdodfo[jfdpojfdspojfdpofjdfodjofds]]')

    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


class NewDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


@permission_required('news.add_post',
                     'news.change_post',
                     'news.view_post', )
def create_new(reguest):
    form = NewsForm
    if reguest.method == "POST":
        form = NewsForm(reguest.POST)
        if form.is_valid():
            post = form.save()
            if '/smi/' in reguest.path:
                Post.WIT = 'NW'
            elif 'article/' in reguest.path:
                Post.WIT = 'AR'

            header = post.header
            text = post.text
            subscribers_email = []

            categoris = post.category.all()
            for cagegory in categoris:
                subscribers_users = cagegory.subscribers.all()
                for sub_users in subscribers_users:
                    subscribers_email.append(sub_users.email)

            html_content = render_to_string('sub.html', {'post': post})
            msg = EmailMultiAlternatives(
                subject=header,
                body=text,
                from_email='mrmolocko@yandex.ru',
                to=subscribers_email
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()
            return HttpResponseRedirect('/news/')

    return render(reguest, 'news_edit.html', {"form": form})


class NewUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.view_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        if 'smi/' in self.request.path:
            Post.WIT = 'NW'
        elif 'article/' in self.request.path:
            Post.WIT = 'AR'
        return super().form_valid(form)


class NewDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        Post = form.save(commit=False)
        if 'smi/' in self.request.path:
            Post.WIT = 'NW'
        elif 'article/' in self.request.path:
            Post.WIT = 'AR'
        return super().form_valid(form)


class news_search(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-id'
    context_object_name = 'news'
    template_name = 'news_search.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def Author_make(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/news/')


@login_required
def category_view(request, pk):
    context = {
        'posts': Post.objects.filter(category__id=pk),
    }
    if request.method == 'POST':
        user = request.user
        action = request.POST.get("confirm")
        if action:
            category = Category.objects.get(pk=pk)
            category.subscribers.add(user)
            category.save()
    return render(request=request, template_name='category.html', context=context)


class IndexView(View):
    def get(self, request):
        printer.apply_async([10])

        hello.delay()
        # _news()
        return HttpResponse('Hello!')
