from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'header',
            'text',
            'category',

        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("header")
        description = cleaned_data.get("text")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
