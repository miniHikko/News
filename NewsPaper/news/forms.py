from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user


class NewsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'post_Author',
            'header',
            'text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("header")
        text = cleaned_data.get("text")

        if name == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
