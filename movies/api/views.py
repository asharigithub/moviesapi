from django.shortcuts import render
from rest_framework.views import APIView
from .models import Movies
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response #the special redirect method of api , the object of which is taken
from .serializer import*
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.decorators import action

class MovieList(APIView):
    def get(self,request,*args,**kwargs):
        mvs=Movies.objects.all()
        ser=MovieSerializer(mvs,many=True)
        
        return Response(data=ser.data)
    def post(self,request,*args,**kwargs):
        mv=request.data
        ser=MovieSerializer(data=mv)
        if ser.is_valid():
            name=ser.validated_data.get("name")
            yr=ser.validated_data.get("year")
            dir=ser.validated_data.get("director")
            genre=ser.validated_data.get("genre")
            Movies.objects.create(name=name,year=yr,director=dir,genre=genre)
            return Response({"msg":"OK"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_417_EXPECTATION_FAILED)


    
class MovieItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("mid")
        mv=Movies.objects.get(id=id)
        ser=MovieSerializer(mv)
        return Response(data=ser.data)
    
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("mid")
        mv=Movies.objects.get(id=id)
        mv.delete
        return Response({"msg":"movie deletion completed"})

        
    def put(self,request,*args,**kwargs):
        id=kwargs.get("mid")
        mv=Movies.objects.get(id=id)
        moviedata=request.data  
        ser=MovieSerializer(data=moviedata)
        if ser.is_valid():
            mv.name=ser.validated_data.get("name")
            mv.year=ser.validated_data.get("year")
            mv.director=ser.validated_data.get("director")
            mv.genre=ser.validated_data.get("genre")
            mv.save()
            return Response({"msg":"updation completed "})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_404_NOT_FOUND)

class MovieModelItem(APIView):
    def get(self,request,*args,**kwargs):
        mvs=Movies.objects.all()
        dser=MoviesModelSer(mvs,many=True)
        return Response(data=dser.data)
    def post(self,request,*args,**kwargs):
        mvs=request.data
        ser=MoviesModelSer(data=mvs)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"created"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_404_NOT_FOUND)
        
class MovieMItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("mid")
        try:
            mv=Movies.objects.get(id=id)
            dser=MoviesModelSer(mv)
            return Response(data=dser.data)
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("mid")
        try:
            mv=Movies.objects.get(id=id)
            mv.delete()
            return Response({"msg":"deletion completed"})
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("mid")
        mv=Movies.objects.get(id=id)
        ser=MoviesModelSer(data=request.data,instance=mv)
        if ser.is_valid():
                ser.save()
                return Response({"msg":"updated"})
        else:
                return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
class UserCreationView(APIView):
    def post(self,request,*args,**kwargs):
        ser=UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"registration completd"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)



#using vieset
class MovieApi(ViewSet):
    def list(self,request,*args,**kwargs):
        mv=Movies.objects.all()
        dser=MoviesModelSer(mv,many=True)
        return Response(data=dser.data)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            mv=Movies.objects.get(id=id)
            dser=MoviesModelSer(mv)
            return Response(data=dser.data)
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request,*args,**kwargs):
        ser=MoviesModelSer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"movie updated"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mv=Movies.objects.get(id=id)
        ser=MoviesModelSer(data=request.data,instance=mv)
        if ser.is_valid():
                ser.save()
                return Response({"msg":"updated"})
        else:
                return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Movies.objects.filter(id=id).delete()
            return Response({"msg":"deletion completed"})
        except:
            return Response({"msg":"invalid id"},status=status.HTTP_404_NOT_FOUND)

#using model viewset
#mvapi/2/get_reviews
#mvapi/2/add_reviews


class MovieApiMV(ModelViewSet):
    serializer_class=MoviesModelSer
    queryset=Movies.objects.all()
    model=Movies
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]

    @action(detail=True, methods=["post"])
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mv=Movies.objects.get(id=id)
        user=request.user
        ser=ReviewSerializers(data=request.data,context={"user":user,"movie":mv})
        if ser.is_valid():
            ser.save()
            return Response({"msg":"added"})
        else:
            return Response({"msg":ser.errors},status=status.HTTP_400_BAD_REQUEST)
    def get_reviews(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mv=Movies.objects.get(id=id)
        review=Reviews.objects.filter(movie=mv)
        dser=ReviewSerializers(review,many=True)
        return Response(data=dser.data)
    




