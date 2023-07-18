import django_filters
from django import forms
from django.forms import DateTimeField
from django_filters import FilterSet, ModelChoiceFilter
from django_filters.fields import IsoDateTimeField

from .models import Post


class MyDateInput(forms.DateInput):
    input_type = 'date'


class NewsFilter(django_filters.FilterSet):
    data_time_gte = django_filters.DateFilter(field_name='data_time', lookup_expr='gte', widget=MyDateInput())

    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'post_Author__user__username': ["icontains"],


        }
