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