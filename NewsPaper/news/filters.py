import django_filters
from django.forms import DateTimeField
from django_filters import FilterSet, ModelChoiceFilter
from django_filters.fields import IsoDateTimeField

from .models import Post


class NewsFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'post_Author__user__username': ["icontains"],
            'data_time': []

        }
