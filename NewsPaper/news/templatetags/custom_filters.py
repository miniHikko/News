from turtledemo.lindenmayer import replace

from django import template

register = template.Library()


@register.filter()
def censor(text):
    list_bad_words = ("Блогеры", "игры")
    over_text = text
    for bad_word in list(list_bad_words):
        over_text = over_text.replace(bad_word, bad_word[:1] + '*' * (len(bad_word) - 1))
    return over_text
