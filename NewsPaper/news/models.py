from builtins import len
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    raiting = models.IntegerField(default=0)

    def uptade_raiting(self):
        Apr = Post.objects.filter(post_Author_id=self.pk).aggregate(r1=Coalesce(Sum('raiting'), 0))['r1']
        Acr = Coment.objects.filter(user_coment_id=self.user).aggregate(r2=Coalesce(Sum('reiting'), 0))['r2']
        Apcr = \
            Coment.objects.filter(post_coment__post_Author__user=self.user).aggregate(r3=Coalesce(Sum('reiting'), 0))[
                'r3']
        self.raiting = Apr * 3 + Acr + Apcr
        self.save()


class Category(models.Model):
    subjiect = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User)


class Post(models.Model):
    Article = "AR"
    New = "NW"
    POSICHEN = [
        (Article, "статья"),
        (New, "новость")
    ]
    post_Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    WIT = models.CharField(max_length=2, choices=POSICHEN)
    # WIT-WhatIsThis
    data_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=50)
    text = models.TextField(max_length=3000)
    raiting = models.IntegerField(default=0)

    def Like(self):
        self.raiting += 1
        self.save()

    def DisLike(self):
        self.raiting -= 1
        self.save()

    def preview(self):
        return self.text[:125] + '...' if len(self.text) > 124 else self.text

    def __str__(self):
        return f'{self.header.title()}: {self.text[:20]}({self.raiting})'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Coment(models.Model):
    post_coment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_coment = models.ForeignKey(User, on_delete=models.CASCADE)
    coment_text = models.TextField(max_length=3000)
    date_time = models.DateTimeField(auto_now_add=True)
    reiting = models.IntegerField(default=0)

    def Like(self):
        self.reiting += 1
        self.save()

    def DisLike(self):
        self.reiting -= 1
        self.save()
