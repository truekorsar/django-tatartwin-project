from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TatarSerializer, TatarFullSerializer, WordErrorCheckSerializer
from apps.core.models import Tatar


def check_error(func):
    def wrapper(*args, **kwargs):
        error_checker = WordErrorCheckSerializer(data={'error': kwargs['word']})
        if not error_checker.is_valid():
            return Response(error_checker.errors, status=status.HTTP_400_BAD_REQUEST)
        return func(*args, **kwargs)
    return wrapper


class TatarRetrieveAPI(APIView):
    @check_error
    def get(self, request, word):
        tatar = Tatar.objects.find_twin(word)
        tatar_serializer = TatarSerializer(tatar)
        return Response(tatar_serializer.data)


class TatarFullRetrieveAPI(APIView):
    @check_error
    def get(self, request, word):
        tatar = Tatar.objects.find_twin(word)
        tatar_serializer = TatarFullSerializer(tatar)
        return Response(tatar_serializer.data)


class TatarTopAPI(APIView):
    def get(self, request, number):
        tatars = Tatar.objects.top(number)
        tatar_serializer = TatarSerializer(tatars, many=True)
        return Response(tatar_serializer.data)


def api_spec(request):
    domain = get_current_site(request).domain
    return render(request, 'restapi/specification.html', {'domain': domain})



