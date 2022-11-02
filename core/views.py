from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.status import *
from django.core.serializers import serialize
import json
from core.models import *
from datetime import datetime

# Create your views here.
class DirectorView(APIView):
    def get(self, request, director_id=None):
        if director_id:
            if Director.objects.filter(pk=director_id).exists():
                director_response = Director.objects.filter(pk=director_id)     # QuerySet
            else:
                return HttpResponse(content_type='application/json',
                                    content=json.dumps({'detail': 'Director not found'}),
                                    status=HTTP_404_NOT_FOUND)
        else:
            director_response = Director.objects.all()
        director_response = serialize('json', director_response)
        return HttpResponse(content_type='application/json',
                            content=director_response,
                            status=HTTP_200_OK)

    def post(self, request):
        body = json.loads(request.body)
        director, created = Director.objects.get_or_create(**body)  # (director, created)
        if created:
            director.save()
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Director created successfully',
                                                    'data': body}),
                                status=HTTP_201_CREATED)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Director already exists'}),
                            status=HTTP_409_CONFLICT)

    def put(self, request, director_id):
        director = Director.objects.filter(pk=director_id)
        if not director.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Director not found'}),
                                status=HTTP_404_NOT_FOUND)
        body = json.loads(request.body)
        body['last_update'] = datetime.now()
        director.update(**body)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Director updated successfully'}),
                            status=HTTP_200_OK)

    def delete(self, request, director_id):
        director = Director.objects.filter(pk=director_id)
        if not director.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Director not found'}),
                                status=HTTP_404_NOT_FOUND)
        director.delete()
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Director deleted successfully'}),
                            status=HTTP_200_OK)


class CategoryView(APIView):

    def get(self, request, category_id=None):
        if category_id:
            if Category.objects.filter(pk=category_id).exists():
                category_response = Category.objects.filter(pk=category_id)
            else:
                return HttpResponse(content_type='application/json',
                                    content=json.dumps({'detail': 'Category not found'}),
                                    status=HTTP_404_NOT_FOUND)
        else:
            category_response = list(Category.objects.all())
        category_response = serialize('json', category_response)
        return HttpResponse(content_type='application/json',
                            content=category_response,
                            status=HTTP_200_OK)

    def post(self, request):
        body = json.loads(request.body)
        director, created = Category.objects.get_or_create(**body)
        if created:
            director.save()
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Category created successfully',
                                                    'data': body}),
                                status=HTTP_201_CREATED)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Category already exists'}),
                            status=HTTP_409_CONFLICT)

    def put(self, request, category_id):
        category = Category.objects.filter(pk=category_id)
        if not category.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Category not found'}),
                                status=HTTP_404_NOT_FOUND)
        body = json.loads(request.body)
        body['last_update'] = datetime.datetime.now()
        category.update(**body)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Category updated successfully'}),
                            status=HTTP_200_OK)

    def delete(self, request, category_id):
        category = Category.objects.filter(pk=category_id)
        if not category.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Category not found'}),
                                status=HTTP_404_NOT_FOUND)
        category.delete()
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Category deleted successfully'}),
                            status=HTTP_200_OK)


class MovieView(APIView):

    def get(self, request, movie_id=None):
        if movie_id:
            if Movie.objects.filter(pk=movie_id).exists():
                movie_response = Movie.objects.get(pk=movie_id)
            else:
                return HttpResponse(content_type='application/json',
                                    content=json.dumps({'detail': 'Movie not found'}),
                                    status=HTTP_404_NOT_FOUND)
        else:
            movie_response = list(Movie.objects.all())
        return HttpResponse(content_type='application/json',
                            content=json.dumps(movie_response),
                            status=HTTP_200_OK)

    def post(self, request):
        body = json.loads(request.body)
        body['director'] = Director.objects.get(pk=body['director'])
        body['category'] = Category.objects.get(pk=body['category'])
        movie, created = Movie.objects.get_or_create(**body)
        if created:
            movie.save()
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Movie created successfully'}),
                                status=HTTP_201_CREATED)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Movie already exists'}),
                            status=HTTP_409_CONFLICT)

    def put(self, request, movie_id):
        movie = Movie.objects.filter(pk=movie_id)
        if not movie.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Movie not found'}),
                                status=HTTP_404_NOT_FOUND)
        body = json.loads(request.body)
        body['last_update'] = datetime.datetime.now()
        movie.update(**body)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Movie updated successfully'}),
                            status=HTTP_200_OK)

    def delete(self, request, movie_id):
        movie = Movie.objects.filter(pk=movie_id)
        if not movie.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Movie not found'}),
                                status=HTTP_404_NOT_FOUND)
        movie.delete()
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Movie deleted successfully'}),
                            status=HTTP_200_OK)
