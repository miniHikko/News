from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm


class NewsList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


def create_new(reguest):
    form = NewsForm
    if reguest.method == "POST":
        form = NewsForm(reguest.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')
    return render(reguest, 'news_edit.html', {"form": form})


class NewUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.WIT = "NW"
        return super().form_valid(form)


class NewDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.WIT = "NW"
        return super().form_valid(form)


class news_search(ListView):
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
