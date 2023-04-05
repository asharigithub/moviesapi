from django.db import models
from rest_framework import serializers


movies=[
    {"id":1,"name":"spadikam","year":1996,"director":"bhadran","genre":"drama"},
    {"id":2,"name":"500 days of summer","year":1999,"director":"michael","genre":"drama"},
    {"id":3,"name":"greenbook","year":2018,"director":"peter farelly","genre":"drama"},
    {"id":4,"name":"forest gump","year":1994,"director":"robert zemiskes","genre":"drama"},
    {"id":5,"name":"dasavatharam","year":2004,"director":"ks ravikumar","genre":"sci-fi"},


]
class Movies(models.Model):
    name=models.CharField(max_length=100)
    year=models.IntegerField()
    director=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)

    








