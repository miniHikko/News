from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.decorators import permission_required


class NewsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class NewDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


@permission_required('news.add_Post',
                     'news.change_Post',
                     'news.view_Post', )
def create_new(reguest):
    form = NewsForm
    if reguest.method == "POST":
        form = NewsForm(reguest.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')
        if '/smi/' in reguest.path:
            Post.WIT = 'NW'
        elif 'article/' in reguest.path:
            Post.WIT = 'AR'
    return render(reguest, 'news_edit.html', {"form": form})


class NewUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_Post',
                           'news.change_Post',
                           'news.view_Post',)
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
