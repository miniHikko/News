from django import forms
from .models import Post
from django.core.exceptions import ValidationError


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
