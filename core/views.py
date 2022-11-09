from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.status import *
from django.core.serializers import serialize
import json
from core.models import *
from datetime import datetime
from django.db import IntegrityError


# Create your views here.
class DirectorView(APIView):
    def get(self, request, director_id=None):
        if director_id:
            if Director.objects.filter(pk=director_id).exists():
                director_response = Director.objects.filter(pk=director_id)  # QuerySet
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
        category, created = Category.objects.get_or_create(**body)
        if created:
            category.save()
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
        body['last_update'] = datetime.now()
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
        movie_response = serialize('json', movie_response)
        return HttpResponse(content_type='application/json',
                            content=movie_response,
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
        body['last_update'] = datetime.now()
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


class ActorView(APIView):
    def get(self, request, actor_id=None):
        if actor_id:
            if Actor.objects.filter(pk=actor_id).exists():
                actor_response = Actor.objects.filter(pk=actor_id)  # QuerySet
            else:
                return HttpResponse(content_type='application/json',
                                    content=json.dumps({'detail': 'Actor not found'}),
                                    status=HTTP_404_NOT_FOUND)
        else:
            actor_response = Actor.objects.all()
        actor_response = serialize('json', actor_response)
        return HttpResponse(content_type='application/json',
                            content=actor_response,
                            status=HTTP_200_OK)

    def post(self, request):
        body = json.loads(request.body)
        actor, created = Actor.objects.get_or_create(**body)  # (actor, created)
        if created:
            actor.save()
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Actor created successfully',
                                                    'data': body}),
                                status=HTTP_201_CREATED)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Actor already exists'}),
                            status=HTTP_409_CONFLICT)

    def put(self, request, actor_id):
        actor = Actor.objects.filter(pk=actor_id)
        if not actor.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Actor not found'}),
                                status=HTTP_404_NOT_FOUND)
        body = json.loads(request.body)
        body['last_update'] = datetime.now()
        actor.update(**body)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Actor updated successfully'}),
                            status=HTTP_200_OK)

    def delete(self, request, actor_id):
        actor = Actor.objects.filter(pk=actor_id)
        if not actor.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Actor not found'}),
                                status=HTTP_404_NOT_FOUND)
        actor.delete()
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Actor deleted successfully'}),
                            status=HTTP_200_OK)


class CastView(APIView):
    def get(self, request, cast_id=None):
        if cast_id:
            if Cast.objects.filter(pk=cast_id).exists():
                cast_response = Cast.objects.filter(pk=cast_id)  # QuerySet
            else:
                return HttpResponse(content_type='application/json',
                                    content=json.dumps({'detail': 'Cast not found'}),
                                    status=HTTP_404_NOT_FOUND)
        else:
            cast_response = Cast.objects.all()
        cast_response = serialize('json', cast_response)
        return HttpResponse(content_type='application/json',
                            content=cast_response,
                            status=HTTP_200_OK)

    def post(self, request):
        body = json.loads(request.body)
        try:
            cast, created = Cast.objects.get_or_create(**body)
            print('1111111111111111111111111111111111111111111')
        except IntegrityError:
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Wrong actor_id/movie_id'}),
                                status=HTTP_400_BAD_REQUEST)
        if created:
            cast.save()
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Cast created successfully',
                                                    'data': body}),
                                status=HTTP_201_CREATED)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Cast already exists'}),
                            status=HTTP_409_CONFLICT)

    def put(self, request, cast_id):
        cast = Cast.objects.filter(pk=cast_id)
        if not cast.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Cast not found'}),
                                status=HTTP_404_NOT_FOUND)
        body = json.loads(request.body)
        body['last_update'] = datetime.now()
        cast.update(**body)
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Cast updated successfully'}),
                            status=HTTP_200_OK)

    def delete(self, request, cast_id):
        cast = Cast.objects.filter(pk=cast_id)
        if not cast.exists():
            return HttpResponse(content_type='application/json',
                                content=json.dumps({'detail': 'Cast not found'}),
                                status=HTTP_404_NOT_FOUND)
        cast.delete()
        return HttpResponse(content_type='application/json',
                            content=json.dumps({'detail': 'Cast deleted successfully'}),
                            status=HTTP_200_OK)


class MovieViewWithOrm(APIView):

    def get(self, request):
        # Obtener registros cuyo nombre sea exactamente Batman
        queryset_exact_field = list(Movie.objects.filter(name__exact="Batman").values("name",
                                                                                      "synopsis",
                                                                                      "director",
                                                                                      "category"))
        # Obtener registros cuyo nombre sea Batman sin tener en cuenta si es mayúscula o minúscula
        queryset_iexact_field = list(Movie.objects.filter(name__iexact="batman").values("name",
                                                                                        "synopsis",
                                                                                        "director",
                                                                                        "category"))

        queryset_icontains_field = list(Movie.objects.filter(name__icontains="batman").values("name",
                                                                                              "synopsis",
                                                                                              "director",
                                                                                              "category"))

        queryset_foreignkey_field = list(Movie.objects.filter(category__name="Terror").values("name",
                                                                                              "category__name",
                                                                                              "director__last_name"))

        response = {
            'exact_field': queryset_exact_field,
            'iexact_field': queryset_iexact_field,
            'icontains_field': queryset_icontains_field,
            'foreignkey_field': queryset_foreignkey_field
        }
        return HttpResponse(content_type='application/json',
                            content=json.dumps(response),
                            status=HTTP_200_OK)
