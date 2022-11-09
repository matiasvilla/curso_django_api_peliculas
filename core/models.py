import datetime

from django.db import models


# Create your models here.
# Director, Category, Movie
class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


class Category(models.Model):
    key = models.CharField(max_length=50, primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    release_date = models.DateTimeField(default='2000-01-01')   # YYYYY-MM-DD
    synopsis = models.TextField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    movie = models.ManyToManyField(Movie, through='Cast')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


class Cast(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
