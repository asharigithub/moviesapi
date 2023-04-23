from rest_framework import serializers
from .models import*
from django.contrib.auth.models import User

class MovieSerializer(serializers.Serializer):
    name=serializers.CharField()
    year=serializers.IntegerField()
    director=serializers.CharField()
    genre=serializers.CharField()
   

class MoviesModelSer(serializers.ModelSerializer):
    class Meta:
        model=Movies
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","password","email"]
    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)
    
class MovieSer(serializers.ModelSerializer):
    class Meta:
        model=Movies
        fields=["movie","year"]

class UserRevSer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","username"]
    
class ReviewSerializers(serializers.ModelSerializer):
    movie=MovieSer(read_only=True)
    user=UserRevSer(read_only=True)
    class Meta:
        model=Reviews
        field=["review","rating","movie","user"]
    def create(self, validated_data):
        user=self.context.get("user")
        mv=self.context.get("movie")
        return Reviews.objects.create(**validated_data,user=user,movie=mv)

    